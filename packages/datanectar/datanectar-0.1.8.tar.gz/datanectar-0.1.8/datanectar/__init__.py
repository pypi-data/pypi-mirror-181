import os
import sys
import json
import pathlib
import hashlib
import logging
import luigi
import luigi.contrib.s3 as luigi_s3

# Basic config
DATANECTAR_CONFIG_FILENAME = 'datanectar.json'
DATANECTAR_LOG_FILENAME = 'datanectar.log'
DATANECTAR_LOG_PATH = os.path.abspath(DATANECTAR_LOG_FILENAME)
TASK_PARAMS_FILENAME = 'task_params.json'



def get_datanectar_config(root):
    root_path = pathlib.Path(root) / DATANECTAR_CONFIG_FILENAME
    if root_path.exists():
        with open(root_path, 'r') as f:
            return json.load(f)
    else:
        return {}


def get_task_files(root):
    task_list = []
    for p in pathlib.Path(root).glob('*/*task.py'):
        task_list.append(p)
    return task_list


def get_task_names_in_root(root):
    task_paths = get_task_files(root)
    task_list = []
    for task_path in task_paths:
        task_path_str = str(task_path)
        if task_path_str.lower().endswith('.py'):
            task_name = task_path_str[:-len('.py')]
            if task_name.startswith(root):
                task_name = task_name[len(str(root) + '/'):]
            task_list.append(task_name)
    return task_list


def get_task_name(task_obj, endswith='_task.py'):
    """eta/extract_task.py -> 'eta/extract_task"""
    module_str = task_obj.__module__
    if module_str == '__main__':
        fpath = sys.modules[task_obj.__module__].__file__
        parts = fpath.split('/')
        if root:
            rel = parts[parts.index(root):]
            rel[-1] = rel[-1].split('.')[0]
            return '/'.join(rel)
    else:
        return module_str.replace('.', '/')


def get_task_version(task_obj):
    params_dict = task_obj.to_str_params()
    value = json.dumps(params_dict, sort_keys=True).encode()
    return hashlib.md5(value).hexdigest()


def save_task_params_to_s3(s3_output_path, task_obj):
    try:
        params_dict = task_obj.to_str_params()
        params_file_path = f'{s3_output_path}/{TASK_PARAMS_FILENAME}'
        params_json = json.dumps(params_dict, sort_keys=True)
        get_s3_client().put_string(params_json, params_file_path)
    except Exception as e:
        print(f'Error saving task params: {e}')


def get_output_dir(
        root, 
        task_obj, 
        output_type=None, 
        save_args=True, 
        without_version=False,
        local_root=None
        ) -> str:
    """
Directory for a given task object's output
    """
    config = get_datanectar_config(root)
    if not output_type:
        output_type = config.get('output_type', 'local')

    task_name = get_task_name(task_obj)
    task_version = get_task_version(task_obj)

    # Option to leave off the version hash, which is useful for storing a "latest" in the task_name dir
    if without_version:
        relative_path = task_name
    else:
        relative_path = f'{task_name}/{task_version}'

    if output_type == 'local':
        output_dir = relative_path
        if save_args:
            os.makedirs(output_dir, exist_ok=True)
            params_file_path = f'{output_dir}/{TASK_PARAMS_FILENAME}'
            params_dict = task_obj.to_str_params()
            with open(params_file_path, 'w') as f:
                json.dump(params_dict, f, sort_keys=True)

        if local_root:
            return local_root + '/' + output_dir


    elif output_type == 's3':
        bucket = config.get('bucket', 'datanectar')
        is_env = config.get('is_env', False)
        if is_env:
            bucket = os.getenv(bucket)
        output_dir = f's3://{bucket}/{relative_path}'

        if save_args:
            save_task_params_to_s3(output_dir, task_obj)

    return output_dir


def get_datanectar_env_vars():
    datanectar_env_vars = {}
    for env_var_name, env_var_value in os.environ.items():
        if env_var_name.startswith('DN_'):
            datanectar_env_vars[env_var_name] = env_var_value
    return datanectar_env_vars


def get_s3_client():
    dn_env_vars = get_datanectar_env_vars()
    if 'DN_AWS_ACCESS_KEY_ID' in dn_env_vars and 'DN_AWS_SECRET_ACCESS_KEY' in dn_env_vars:
        aws_access_key = dn_env_vars['DN_AWS_ACCESS_KEY_ID']
        aws_secret_key = dn_env_vars['DN_AWS_SECRET_ACCESS_KEY']
        s3client = luigi_s3.S3Client(aws_access_key, aws_secret_key)
        return s3client
    return None


def get_luigi_output_target(root, task_obj, output_type=None, filename=None, without_version=False):
    config = get_datanectar_config(root)
    output_path = get_output_dir(root, task_obj, output_type, without_version=without_version)
    if filename:
        output_path = f'{output_path}/{filename}'

    if not output_type:
        if 'output_type' in config:
            output_type = config['output_type']
        else:
            output_type = 's3'

    if output_type == 'local':
        return luigi.LocalTarget(output_path)
    elif output_type == 's3':
        bucket_name = config.get('bucket', 'datanectar')
        return luigi_s3.S3Target(output_path, client=get_s3_client())


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root', action='store', default='test_root')
    args = parser.parse_args()
    root = args.root

    print(f'Datanectar root: {root}')

    dn_config = get_datanectar_config(root)
    print(f'\nDatanectar config (in root={root}): {dn_config}')

    task_files = get_task_files(root)
    print(f'\nTask files (in root={root}): {task_files}')

    task_list = get_task_names_in_root(root)
    print(f'\nTask names (in root={root}): {task_list}')

    # Testing calling datanectar and passing in Luigi task
    if root == 'test_root':
        sys.path.append(root)
        import datetime
        import etl.extract_task
        import etl.rollup_task
        extract_task = etl.extract_task.ExtractTask()
        rollup_task = etl.rollup_task.RollupTask()
        output_dir = get_output_dir(root, extract_task)
        print(f'output_dir for {extract_task}: {output_dir}')
        output_dir2 = get_output_dir(root, rollup_task)
        print(f'output_dir for {rollup_task}: {output_dir2}')

        output_dir3 =  get_output_dir(root, rollup_task, output_type='local')
        print(f'output_dir for {rollup_task} (for output_type=local) = {output_dir3}')

        task_version = get_task_version(rollup_task)
        print(f'task_version for {rollup_task}: {task_version}')

        rollup_task_date = etl.rollup_task.RollupTask(date_param=datetime.date(2022, 1, 10))
        output_dir_date = get_output_dir(root, rollup_task_date, output_type='s3')
        print(f'output_dir for {rollup_task_date}: {output_dir_date}')

        output_dir_without_version= get_output_dir(root, rollup_task_date, output_type='s3', without_version=True)
        print(f'output_dir without version for {rollup_task_date}: {output_dir_without_version}')

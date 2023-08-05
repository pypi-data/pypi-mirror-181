import datatools

# stub = 'cloud-data-service-test.sanywind.net:50051'
# dt = datatools.DataTools()
# wf = datatools.WindFarmInf(graphql_url='https://graphql.sanywind.net/graphql', use_grapql=True)
# df = wf.get_power_curve_by_turbine('NXFC', '101')
# print(df)
# # dt.download_files(stub, 'model_test/1.html', save_path='../sanydata/test')
# columns = ['project_name', 'project_version', 'pinyin_code', 'turbine_name', 'result']
# df = dt.get_model_result(stub, project_name='yaw_error', farm='TYSFCB', turbine='001',
#                     data_start_time_list=['2022-01-25', '2022-08-02'], columns=columns)
# print(df)

ds = datatools.SanyLog(project_name='test', project_version='0.0.1', author='tianh9')


def f(b, farm):
    a = 1/b
    return a


def f1(b):
    a = f(b, 'TYSFCH')
    return a
extra_str = {'cost_time': 11.935047, 'data_type': 'qd', 'paramater': {'date123': '2022-12-07 19:59:03', 'file_type': 'qd', 'func_name': 'sgm_aero', 'func_status': 'success', 'func_version': '1.0.0', 'path': 'semi/data/HJLFCB/plc-sync/20221207/qd/csv/HJLFCB_066_2022_12_07_19_59_03_A_1749_13_qd.csv', 'pinyin_code': 'HJLFCB', 'record_time': '2022-12-08 19:25:37', 'turbine_num': '066', 'upload_path': ''}}
ds.info('trans_test', 'farm', 'turbine', extra=extra_str)

# try:
#     c = f1(0)
# except Exception as e:
#     ds.error(e, 'TYSFCH', '004')


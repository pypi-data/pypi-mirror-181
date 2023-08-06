#!/share/nas2/genome/biosoft/Python//3.7.3/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/12/6 15:41
# @Author : jmzhang
# @Email : zhangjm@biomarker.com.cn


import spatial_tools
import argparse

if __name__ == '__main__':
    desc = """
    Version: Version beta
    Contact: zhangjm <zhangjm@biomarker.com.cn>
    Program Date: 2022.10.25
    Description: spatial tools
    """

    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--port', type=int, help='port', default=5070)
    input_args = parser.parse_args()

    spatial_tools.SpatialApp.run_dash(port=input_args.port, debug=False)



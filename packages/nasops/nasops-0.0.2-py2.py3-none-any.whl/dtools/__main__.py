import argparse as arg
import os

from .util import download_from_nas, list_file, upload

def bmcompiler_parser():
    parser = arg.ArgumentParser(description     = "handle nas with command line",
                                formatter_class = arg.ArgumentDefaultsHelpFormatter,
                                prog            = "python -m dtools")
    
    parser.add_argument("method", choices=["download", "upload", "list"], help="download or upload")
    
    # upload file argments : name, password, local_dir, nas_dir
    parser.add_argument("--name", type=str,help="username")
    parser.add_argument("--password", type=str,help="password")
    parser.add_argument("--local_dir", type=str,help="local dir")
    parser.add_argument("--nas_dir", type=str,help="nas dir. Attention : \n \
        1. if the nas_dir is not exist, it will be created automatically. \n \
        2. And usually you should set nas_dir as /home/Drive/xxxx. \n \
        3. upload mode and target name is not support now. ")
    parser.add_argument('--verbose', type=bool, default=False, help='verbose')
    return parser

if __name__ == "__main__":
    parser = bmcompiler_parser()
    a = parser.parse_args()
    

    if a.method == 'download':
        download_from_nas(a.url)
    
    if a.method == 'upload':
        upload(a.name, a.password, a.local_dir, a.nas_dir)
        
    if a.method == 'list': 
        list_file(a.name, a.password, a.nas_dir)
    
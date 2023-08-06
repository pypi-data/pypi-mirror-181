1. python setup.py sdist bdist_wheel --universal
2. twine upload dist/*


## support ops:  
1. download file 
`dtools download --url xxxxxx`   
1. upload file / dir  
`dtools upload --name wangyang.zuo --password xxxxxx --local_dir xxxx --nas_dir xxxx`   
1. list file / dir 
`dtools list--name wangyang.zuo --password xxxxxx --nas_dir xxxx`   
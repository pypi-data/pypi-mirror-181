# -*- coding: utf-8 -*-
import os
from oss2 import SizedFileAdapter, determine_part_size
from oss2.models import PartInfo
import oss2

# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth('yourAccessKeyId', 'yourAccessKeySecret')
# Endpoint以华东1（杭州）为例，其他Region请按实际情况填写。
# 填写Bucket名称，例如examplebucket。
bucket = oss2.Bucket(auth, 'https://oss-cn-hangzhou.aliyuncs.com', 'examplebucket')
# 填写不能包含Bucket名称在内的Object完整路径，例如exampledir/exampleobject.txt。
key = 'exampledir/exampleobject.txt'
# 填写本地文件的完整路径，例如D:\\localpath\\examplefile.txt。
filename = 'D:\\localpath\\examplefile.txt'

total_size = os.path.getsize(filename)
# determine_part_size方法用于确定分片大小。
part_size = determine_part_size(total_size, preferred_size=100 * 1024)

# 初始化分片。
# 如需在初始化分片时设置文件存储类型，请在init_multipart_upload中设置相关Headers，参考如下。
# headers = dict()
# 指定该Object的网页缓存行为。
# headers['Cache-Control'] = 'no-cache'
# 指定该Object被下载时的名称。
# headers['Content-Disposition'] = 'oss_MultipartUpload.txt'
# 指定该Object的内容编码格式。
# headers['Content-Encoding'] = 'utf-8'
# 指定过期时间，单位为毫秒。
# headers['Expires'] = '1000'
# 指定初始化分片上传时是否覆盖同名Object。此处设置为true，表示禁止覆盖同名Object。
# headers['x-oss-forbid-overwrite'] = 'true'
# 指定上传该Object的每个Part时使用的服务器端加密方式。
# headers[OSS_SERVER_SIDE_ENCRYPTION] = SERVER_SIDE_ENCRYPTION_KMS
# 指定Object的加密算法。如果未指定此选项，表明Object使用AES256加密算法。
# headers[OSS_SERVER_SIDE_DATA_ENCRYPTION] = SERVER_SIDE_ENCRYPTION_KMS
# 表示KMS托管的用户主密钥。
# headers[OSS_SERVER_SIDE_ENCRYPTION_KEY_ID] = '9468da86-3509-4f8d-a61e-6eab1eac****'
# 指定Object的存储类型。
# headers['x-oss-storage-class'] = oss2.BUCKET_STORAGE_CLASS_STANDARD
# 指定Object的对象标签，可同时设置多个标签。
# headers[OSS_OBJECT_TAGGING] = 'k1=v1&k2=v2&k3=v3'
# upload_id = bucket.init_multipart_upload(key, headers=headers).upload_id
upload_id = bucket.init_multipart_upload(key).upload_id
parts = []

# 逐个上传分片。
with open(filename, 'rb') as fileobj:
    part_number = 1
    offset = 0
    while offset < total_size:
        num_to_upload = min(part_size, total_size - offset)
        # 调用SizedFileAdapter(fileobj, size)方法会生成一个新的文件对象，重新计算起始追加位置。
        result = bucket.upload_part(key, upload_id, part_number,
                                    SizedFileAdapter(fileobj, num_to_upload))
        parts.append(PartInfo(part_number, result.etag))

        offset += num_to_upload
        part_number += 1

# 完成分片上传。
# 如需在完成分片上传时设置相关Headers，请参考如下示例代码。
headers = dict()
# 设置文件访问权限ACL。此处设置为OBJECT_ACL_PRIVATE，表示私有权限。
# headers["x-oss-object-acl"] = oss2.OBJECT_ACL_PRIVATE
bucket.complete_multipart_upload(key, upload_id, parts, headers=headers)
# bucket.complete_multipart_upload(key, upload_id, parts)

# 验证分片上传。
with open(filename, 'rb') as fileobj:
    assert bucket.get_object(key).read() == fileobj.read()

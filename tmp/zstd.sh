#!/bin/bash

bucket_name="voices-kw-dataset"
bucket_path="s3://voices-kw-dataset/karanovc/"

# データをダウンロードするPath
local_dir="/home/ubuntu/data"

# ダウンロード範囲（ここでは、jvs001~100）
# start_index=1
# end_index=100


# folders=$(aws s3 ls "$bucket_path" --endpoint-url=https://s3.ap-northeast-2.wasabisys.com| awk '{print $4}')


# # 각 폴더별로 처리
# for folder_name in $folders; do
#     if [[ "$folder_name" == jvs* ]]; then
#         continue
#     fi
#     # CLI 다운로드
#     aws s3 cp "s3://voices-kw-dataset/karanovc/$folder_name" "$local_dir" --endpoint-url=https://s3.ap-northeast-2.wasabisys.com
# done


# # Extract all tar.zst files into Local_Dir
for file in "$local_dir"/*.tar.zst; do
  # Print
#   file = "/home/ubuntu/data/k小山美光.tar.zst"
  echo "Extracting $file..."
  
  # Execute zstd
  zstd -dc "$file" | tar -xf - -C "$local_dir"

  # Print
  echo "Removing $file..."
  
  # Remove *.tar.zst  
  rm "$file"
done


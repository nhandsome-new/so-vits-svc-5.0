#!/bin/bash

bucket_name="voices-kw-dataset"
bucket_path="s3://voices-kw-dataset/karanovc/"

# データをダウンロードするPath
local_dir="/home/ubuntu/data"

# ダウンロード範囲（ここでは、jvs001~100）
start_index=1
end_index=10


# folders=$(aws s3 ls "$bucket_path" --endpoint-url=https://s3.ap-northeast-2.wasabisys.com| awk '{print $4}')


# # 각 폴더별로 처리
# for folder_name in $folders; do
#     if [[ "$folder_name" == jvs* ]]; then
#         continue
#     fi
#     # CLI 다운로드
#     aws s3 cp "s3://voices-kw-dataset/karanovc/$folder_name" "$local_dir" --endpoint-url=https://s3.ap-northeast-2.wasabisys.com
# done









# # Local_dir 生成
mkdir -p "$local_dir"

# # # For Loop for Download
# for ((i=start_index; i<=end_index; i++))
# do
#     # Folder Name (jvs001, jvs002, ... ,jvs100)
#     folder_name="jvs$(printf "%03d" $i)"

#     # Download CLI
#     aws s3 cp "s3://voices-kw-dataset/karanovc/$folder_name.tar.zst" "$local_dir" --endpoint-url=https://s3.ap-northeast-2.wasabisys.com

# done


# Extract all tar.zst files into Local_Dir
# for file in "$local_dir"/*.tar.zst; do
#   # Print
#   echo "Extracting $file..."
  
#   # Execute zstd
#   zstd -dc "$file" | tar -xf - -C "$local_dir"
# done

# Delete all tar.zst files
for file in "$local_dir"/*.tar.zst; do
  # Print
  echo "Removing $file..."
  
  # Remove *.tar.zst  
  rm "$file"
done
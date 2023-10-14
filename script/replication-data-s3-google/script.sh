for obj in $(aws s3 ls s3://pilha-nuvem-tcc-sptech-bucket/ | awk '{print $4}'); do
  gsutil rsync -d -r "s3://pilha-nuvem-tcc-sptech-bucket/$obj" "gs://bucket-data-replication-aws-s3/$obj"
done
#!/bin/bash
# Production backup script

BACKUP_DIR="/backups/kbi-labs/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker exec postgres pg_dump -U user kbi_prod | gzip > $BACKUP_DIR/postgres_backup.sql.gz

# Backup Redis
docker exec redis redis-cli BGSAVE
docker cp redis:/data/dump.rdb $BACKUP_DIR/redis_backup.rdb

# Backup application logs
tar -czf $BACKUP_DIR/logs_backup.tar.gz /var/log/kbilabs/

# Upload to S3
aws s3 sync $BACKUP_DIR s3://kbi-labs-backups/$(date +%Y%m%d_%H%M%S)/

# Clean up old backups (keep last 30 days)
find /backups/kbi-labs -mtime +30 -type d -exec rm -rf {} +

echo "Backup completed: $BACKUP_DIR"

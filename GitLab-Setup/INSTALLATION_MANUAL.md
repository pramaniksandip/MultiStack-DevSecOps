# GitLab Migration & Restoration Guide

This documentation provides a comprehensive, technical walkthrough for installing and restoring a **self-managed GitLab instance** using Docker. This guide is specifically designed for environments requiring high-fidelity data restoration, such as the **Unified DevSecOps Platform**.

---

## 📋 Prerequisites

Before commencing the restoration, ensure the host system satisfies these technical requirements:

* **Operating System:** Linux-based server (e.g., AlmaLinux, CentOS, or Ubuntu).
* **Container Engine:** Latest version of **Docker** and **Docker Compose** installed and running.
* **Storage:** At least 4GB of free space to accommodate the Docker image (~3.6GB) and backup archives. And 16GB of space for backup required.
* **Permissions:** Root or sudo access is mandatory for managing container lifecycles and file system permissions.
* **Domain Name:** A valid domain name is required for accessing the service (e.g., gitlab.edu.in). Replace this value with your own domain name as applicable.

---

## 🗂️ Step 1: Resource Acquisition

Acquire the following components from the secure project storage (e.g., Google Drive):

1. **GitLab Docker Image:** [gitlab_gitlab-ce_latest.tar](https://drive.google.com/file/d/18VlFPe_JjluUBM8f8lbOFmPqPjxy67_z/view?usp=sharing) 
2. **GitLab Backup File:** [1769020398_2026_01_21_18.0.2_gitlab_backup.tar](https://drive.google.com/file/d/1IwbwXD7ioql3S1Or-oDhuJcZfEfrAUPn/view?usp=sharing) 
3. **Docker Compose File:** Standardized `docker-compose.yml`.
4. **Configuration Archive:** Existing [Config Folder](https://drive.google.com/file/d/1Oejb2wU4rCEamr7In5GC2LjJtyqDryPx/view?usp=sharing)




---


## 🛠️ Step 2: Environment Setup

Establish the standardized directory structure on the target server.

```bash
# 1. Create the working and data persistence directories
mkdir -p /root/gitlabwork/gitlabdata/

# 2. Place the Docker Compose file in the workspace
# Move your downloaded docker-compose.yml to /root/gitlabwork/

# 3. Transfer the Docker image tarball to the server root
# Move gitlab_gitlab-ce_latest.tar to /root/

```

---

## 🐳 Step 3: Image Loading & Preparation

Since we are performing an offline installation, load the image from the local filesystem.

```bash
# Verify no existing GitLab images
docker images

# Load the image from the tar file
docker load < /root/gitlab_gitlab-ce_latest.tar

# If the image ID (e.g., 54b0f16e19db) does not have a tag, rename it:
docker image tag 54b0f16e19db gitlab/gitlab-ce:latest

# Set the home variable for persistent data storage
export GITLAB_HOME=/root/gitlabwork/gitlabdata/

```

---

## 🚀 Step 4: Initial Deployment & Config Migration

Perform a fresh installation to initialize the container environment, then inject the production configuration.

```bash
# 1. Start the fresh instance
cd /root/gitlabwork/
docker compose up -d

# 2. Verify URL accessibility (Instance will be empty)

# 3. Stop the instance to replace configurations
docker compose down

# 4. Replace the default config with the production archive
cd /root/gitlabwork/gitlabdata/
rm -rf config
cp -r /path/to/downloaded_config_folder ./config

# 5. Restart with the production config
cd /root/gitlabwork/
docker compose up -d

```

---

## 🔄 Step 5: Data Restoration Procedure

Restoring the database and repositories requires stopping the active application services within the container.

### 5.1 Prepare the Backup Archive

```bash
# Create the backup directory
mkdir -p /root/gitlabwork/gitlabdata/data/backups

# Copy the backup file to the target directory
cp /path/to/1769020398_2026_01_21_18.0.2_gitlab_backup.tar /root/gitlabwork/gitlabdata/data/backups/

# Set necessary ownership and permissions
cd /root/gitlabwork/gitlabdata/data/backups/
chmod 600 1769020398_2026_01_21_18.0.2_gitlab_backup.tar
chown 998:998 1769020398_2026_01_21_18.0.2_gitlab_backup.tar

```

### 5.2 Execute Restoration

```bash
# 1. Stop the Puma (Application Server) and Sidekiq (Background Jobs)
docker compose exec web gitlab-ctl stop puma
docker compose exec web gitlab-ctl stop sidekiq

# 2. Verify service status
docker compose exec web gitlab-ctl status

# 3. Run the restore command
# CRITICAL: Exclude '_gitlab_backup.tar' from the filename in the command
docker compose exec web gitlab-backup restore BACKUP=1769020398_2026_01_21_18.0.2

# 4. Restart services
docker compose exec web gitlab-ctl start sidekiq
docker compose exec web gitlab-ctl start puma

# 5. Final check
docker compose exec web gitlab-ctl status

```

---

## ✅ Post-Restoration Checklist

* **Status Check:** Ensure all services return a `run` status via `gitlab-ctl status`.
* **Data Integrity:** Log in to `gitlab.wb.nic.in` to verify project repositories and issues.
* **Authentication:** Verify the `initial_root_password` located in the `config` folder.


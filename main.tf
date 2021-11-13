/*
The below terraform configuration does the following:
   1. Connects to your GCP project via the project name and service account key credentials
   2. Creates the following resources in the US Central region:
      - Virtual network
      - VM instance running debian
      - Virtual firewall that allows SSH connection and incoming HTTP requests from the provided IP addresses
*/

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {
  credentials = file("<path to service account key file>.json")

  project = "<GCP Project ID>"
  region  = "us-central1"
  zone    = "us-central1-c"
}

resource "google_compute_network" "vpc_network" {
  name = "terraform-network"
}

resource "google_compute_instance" "vm_instance" {
  name         = "terraform-instance"
  machine_type = "f1-micro"
  tags = ["linuxadmin"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.name
    access_config {
    }
  }
}

resource "google_compute_firewall" "firewall" {
    name = "test-firewall"
    network = google_compute_network.vpc_network.name

    allow {
        protocol  = "tcp"
        ports     = ["80", "8080", "1000-2000"]
    }

    allow {
        protocol = "tcp"
        ports = ["22", "3389"]
    }

    direction = "INGRESS"

    # The 35.235.240.0/20 range encompasses all IP addresses that IAP (Identity-Aware Proxy - https://cloud.google.com/iap/docs/using-tcp-forwarding) uses for TCP forwarding (thus allowing you to SSH into the VM). If you wish to send HTTP requests to this VM, you will to include the IP address and/or range of IP addresses in this list.
    source_ranges = ["35.235.240.0/20"]
    
    target_tags = ["linuxadmin"]
}
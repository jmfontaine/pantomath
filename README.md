# Pantomath

![Build Status](https://github.com/jmfontaine/pantomath/actions/workflows/build.yml/badge.svg)
![Interrogate](assets/badges/interrogate.svg)

Pantomath is a command-line application that helps you collect, analyze, and explore all the data you need to optimize the cost of your cloud.

## 🎯 Purpose

Pantomath is a versatile data manager that allows to easily:

- Collect data from various sources (**APIs, databases, local and remote files**, web sites, etc.).
- Store structured and semi-structured data.
- Query data with **SQL**.
- Report on the data.
- Alert on the data.

It is designed to be extensible so that adding support for new data sources requires minimal work.

## ⚡️ Getting Started

### Prerequisites

- [Python](https://www.python.org/) 3.7+
- [PostgreSQL](https://www.postgresql.org/) 13+

### Installation

- Clone the repository.

```shell
git clone https://github.com/jmfontaine/pantomath.git
cd pantomath
```

- Install the dependencies with [Poetry](https://python-poetry.org).

```shell
poetry install
```

- Activate the virtual environment.

```shell
poetry shell
```



When done using Pantomath, you can deactivate the Poetry shell:

```shell
exit
```

## 💻 Usage

To start the interactive program, run `pantomath`.

```shell
Usage: pantomath [OPTIONS] COMMAND [ARGS]...

  Easily collect, analyze, and explore FinOps data.

  Written by Jean-Marc Fontaine (jm@jmfontaine.net).

Options:
  -c, --config TEXT  Set configuration file path.  [default: pantomath.yaml]
  -v, --verbose      [x>=0]
  --help             Show this message and exit.

Commands:
  collect  Extract, transform and load from data sources into the database.
  version  Display version.
```

## ⚙️ Configuration

Pantomath can be configured via a YAML configuration.

By default, Pantomath will look in the current folder for a file named `pantomath.yaml`. This can be overridden by using the `--config` option (or `-c` for short): `pantomath --config ./custom/path/pantomath.yaml`.

Here are all the currently available settings:

```yaml
version: 0.1.0

db:
  host: localhost # Optional
  port: 5432 # Optional
  user: pantomath # Optional
  password: pantomath # Optional
  name: pantomath # Optional

providers:
  aws:
    settings:
      accounts:
        - profile: account1
        - profile: account2
          assume_role: arn:aws:iam::1111111111111:role/MyRole
    sources:
      - aws_cloudfront_distributions
      - aws_cloudtrail_trails
      - aws_dax_clusters
      - aws_docdb_clusters
      - aws_dynamodb_tables
      - aws_ebs_snapshots
      - aws_ebs_volumes
      - aws_ec2_alb
      - aws_ec2_clb
      - aws_ec2_eip
      - aws_ec2_glb
      - aws_ec2_images
      - aws_ec2_instances
      - aws_ec2_nat_gateways
      - aws_ec2_nlb
      - aws_ec2_vpc_endpoints
      - aws_ecs_clusters
      - aws_efs_file_systems
      - aws_eks_clusters
      - aws_elasticache_clusters
      - aws_emr_clusters
      - aws_es_domains
      - aws_lambda_functions
      - aws_rds_instances
      - aws_rds_snapshots
      - aws_redshift_clusters
      - aws_route53_domains
      - aws_s3_buckets

```

## 🙋 Support

If you need some help, please [create an issue](https://github.com/jmfontaine/pantomath/issues).

## 🤔 Pantomath?

A [pantomath](https://en.wikipedia.org/wiki/Pantomath) is a person who wants to know or knows everything.

This tool aims at making it easier for users to know everything they need to manage and optimize the cost of their cloud.

## 📜 License

Pantomath is free, and the source is available. It is distributed under the [Server Side Public License (SSPL) v1](LICENSE.txt).

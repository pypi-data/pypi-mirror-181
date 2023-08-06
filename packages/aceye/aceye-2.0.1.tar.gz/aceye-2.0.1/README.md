[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/automateyournetwork/ACEye)

# ACEye

Business Ready Documents for Cisco ACI

## Current API Coverage

Access Bundle Groups

Access Control Entities

Access Control Instances

Access Control Rules

Access Control Scope

Access Policy Group Source Relationships

Access Port Groups

Access Port Profiles

Application Profiles

ARP Adjacency Endpoints

ARP Database

ARP Domain

ARP Entity

ARP Instances

ARP Interfaces

Attachable Access Entity Profiles

Attachable Access Entity Profiles Source Relationships

*Audit Log

BGP Address Families

BGP Domains

BGP Entities

BGP Instances

BGP Instances Policy

BGP Peers

BGP Peers AF Entries

BGP Peers Entries

BGP Route Reflector Policy

BGP Route Reflectors

Bridge Domains

Bridge Domains Target Relationships

Bridge Domains To Outside

CDP Adjacency Endpoints

CDP Entities

CDP Instances

CDP Interface Addresses

CDP Interfaces

CDP Management Addresses

Cluster Aggregate Interfaces

Cluster Health

Cluster Physical Interfaces

Cluster RS Member Interfaces

Compute Controllers

Compute Domains

Compute Endpoint Policy Descriptions

Compute Providers

Compute RS Domain Policies

Context Source Relationships

Contexts (VRFs)

Contexts Target Relationships

Contracts

Contract Consumer Interfaces

Contract Consumers

Contract Consumers Root

Contract Providers

Contract Providers Root

Contract Subjects

Contract Subjects Filter Attributes

Controllers

Device Packages

Domain Attachments

Domain Profile Source Relationships

Endpoint Profile Containers

Endpoints (All Connected Fabric Endpoints)

Endpoints To Paths

EPG to Bridge Domain Links

EPGs (Endpoint Groups)

Equipment Board Slots

Equipment Boards

Equipment Chassis

Equipment CPUs

Equipment DIMMs

Equipment Fabric Extenders

Equipment Fabric Ports

Equipment Fan Slots

Equipment Fan Trays

Equipment Fans

Equipment Field Programmable Gate Arrays

Equipment Indicator LEDs

Equipment Leaf Ports

Equipment Line Card Slots

Equipment Line Cards

Equipment Port Locator LEDs

Equipment Power Supplies

Equipment Power Supply Slots

Equipment RS IO Port Physical Configs

Equipment Sensors

Equipment SP Common Blocks

Equipment SPROM LCs

Equipment SPROM Power Supplies

Equipment SPROM Power Supply Blocks

Equipment SPROM Supervisors

Equipment Storage

Equipment Supervisor Slots

Equipment Supervisors

Ethernet Port Manager Physical Interfaces

*Events

External Unmanaged Nodes

External Unmanaged Nodes Interfaces

Fabric Extended Path Endpoint Containers

Fabric Instances

Fabric Link Containers

Fabric Links

Fabric Loose Links

Fabric Loose Nodes

Fabric Membership

Fabric Node SSL Certifcates

Fabric Nodes

Fabric Path Endpoint Containers

Fabric Path Endpoints

Fabric Paths

Fabric Pods

Fabric Protected Path Endpoint Containers

Fault Summary

FEX Policies

Fibre Channel Entity

Firmware Card Running

Firmware Compute Running

Firmware Running

Function Policies

Health

Host Port Selectors

Interface Policies

Interface Profiles

IP Addresses

IPv4 Addresses

IPv4 Domains

IPv4 Entities

IPv4 Instances

IPv4 Interfaces

IPv4 Next Hop

IPv4 Routes

ISIS Adjacency Endpoints

ISIS Discovered Tunnel Endpoints

ISIS Domains

ISIS Domains Level

ISIS Entities

ISIS Instances

ISIS Interfaces

ISIS Interfaces Level

ISIS Next Hop

ISIS Routes

L2 Bridge Domains

L2 EPG Bridge Domain Source Relationships

L2 External Instance Profiles

L2 External Interfaces

L2 External Logical Interface Profiles

L2 External Logical Node Profiles

L2 Interface Source Relationships

L2Out Paths

L2Outs

L3 Contexts

L3 Contexts Source Relationships

L3 Domains

L3 Domains Source Relationships

L3 Instances

L3 Interfaces

L3 Logical Interface Profiles

L3 Logical Node Profiles

L3 Physical Interface Source Relationships

L3 Routed Interfaces

L3 Routed Loopback Interfaces

L3 Subinterfaces

L3 Subnets

L3Out IP Addresses

L3Out Members

L3Out Node Source Relationships

L3Out Path Source Relationships

L3Out Profiles

L3Outs

LACP Entities

LACP Instances

LACP Interfaces

Leaf Interface Profiles

Leaf Switch Profiles

License Entitlements

LLDP Adjacency Endpoints

LLDP Entities

LLDP Instances

LLDP Interfaces

Locales

Management Interfaces

OSPF Adjacency Endpoints

OSPF Areas

OSPF Database

OSPF Domains

OSPF Entities

OSPF External Profiles

OSPF Instances

OSPF Interfaces

OSPF Routes

OSPF Unicast Next Hop

Path Attachments

Physical Domains

Physical Interfaces

Port Blocks

Port Channel Aggregate Interfaces

Port Channel Member Interfaces

Prefix List

Prefix List Detailed

QOS Classes

Route Policies

Security Domains

Spine Access Policy Groups

Spine Access Port Profiles

Spine Host Port Selectors

Spine Interface Profiles

Spine Switch Profiles

Static Route Next Hop Policies

Subnets

SVIs

Tenant

Tenant Health

Top System

Tunnel Interfaces

Unicast Route Database

Unicast Route Domains

Unicast Route Entities

Unicast Route Next Hop

Unicast Routes

Users

VLAN Encapsulation Blocks

VLAN Endpoint Group Encapsulation

VLAN Namespace Policies

VLAN Namespace Source Relationships

VLAN Pools

VMM Controller Profiles

VMM Domain Profiles

VMM Provider Profiles

VMM User Profiles

VPC Configurations

VPC Domains

VPC Entities

VPC Instances

VPC Interfaces

vzAny

vzAny To Consumers

vzAny To Providers

vzDeny Rules

vzEntries

vzFilters

vzInterface Source Relationships

vzRule Owner

vzTaboo

Wired Nodes

* Both Audit Log and Events are commented out of the base package due to the potentially huge number of records; should you want the Audit Log / Events please uncomment out lines 72-73 (Audit Log) and 76-77 (Events)


## Installation

```console
$ python3 -m venv ACI
$ source ACI/bin/activate
(ACI) $ pip install aceye
```

## Usage - Help

```console
(ACI) $ aceye --help
```

![ACEye Help](/images/help.png)

## Usage - In-line

```console
(ACI) $ aceye --url <url to APIC> --username <APIC username> --password <APIC password>
```

## Usage - Interactive

```console
(ACI) $ aceye
APIC URL: <URL to APIC>
APIC Username: <APIC Username>
APIC Password: <APIC Password>
```

## Usage - Environment Variables

```console
(ACI) $ export URL=<URL to APIC>
(ACI) $ export USERNAME=<APIC Username>
(ACI) $ export PASSWORD=<APIC Password>
```

## Recommended VS Code Extensions

Excel Viewer - CSV Files

Markdown Preview - Markdown Files

Markmap - Mindmap Files

Open in Default Browser - HTML Files

## Contact

Please contact John Capobianco if you need any assistance

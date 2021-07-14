switch_setup_show = """
    switch-name:               119-NRU02-spine-01
    mgmt-ip:                   21.119.28.11/19
    mgmt-ip-assignment:        static
    mgmt-ip6:                  fe80::491:2aff:fe26:ffaf/64
    mgmt-ip6-assignment:       autoconf
    mgmt-link-state:           up
    mgmt-link-speed:           1g
    in-band-ip:                169.254.119.11/24
    in-band-ip6:               fe80::640e:94ff:fe4f:1c24/64
    in-band-ip6-assign:        autoconf
    gateway-ip:                21.119.31.254
    dns-ip:                    21.255.254.45
    dns-secondary-ip:          21.255.254.46
    domain-name:               domain.com
    ntp-server:                21.255.254.13
    ntp-secondary-server:      21.255.254.14
    timezone:                  Europe/Stockholm
    date:                      2021-07-09,13:13:39
    hostid:                    285212751
    location-id:               4
    enable-host-ports:         yes
    motd:                      LINUX TRACK - 6.1.0 HF4
    banner:                    LINUX TRACK - 6.1.0 HF4
    mgmt-lag:                  active-standby
    mgmt-lacp-mode:            off
    ntp:                       on
    """

vlan_show = """
119-NRU02-spine-01 1    public no         none        local default-1   yes    yes   2-4,6-8,10-12,14-16,18-20,22-24,26-28,30-130 2-4,6-8,10-12,14-16,18-20,22-24,26-28,
30-129 129               
119-NRU02-spine-01 3800 public no         none        local vlan-3800   yes    yes   1,129                                        1                                     
       1,129             
119-NRU02-spine-01 3801 public no         none        local vlan-3801   yes    yes   5,129                                        5                                     
       5,129             
119-NRU02-spine-01 3802 public no         none        local vlan-3802   yes    yes   9,129                                        9                                     
       9,129             
119-NRU02-spine-01 3803 public no         none        local vlan-3803   yes    yes   13,129                                       13                                    
       13,129            
119-NRU02-spine-01 3804 public no         none        local vlan-3804   yes    yes   17,129                                       17                                    
       17,129            
119-NRU02-spine-01 3805 public no         none        local vlan-3805   yes    yes   21,129                                       21                                    
       21,129            
119-NRU02-spine-01 3806 public no         none        local vlan-3806   yes    yes   25,129                                       25                                    
       25,129            
119-NRU02-spine-01 3807 public no         none        local vlan-3807   yes    yes   29,129                                       29                                    
       29,129            
119-NRU02-spine-01 4093 public no         none        local vlan-4093   yes    yes   397                                          397                                   
       none
"""

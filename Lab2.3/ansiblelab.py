- hosts: fs-ga
  tasks:
    - name: show total packets
      command: ifconfig -a
      register: interfaces

    - name: filter
      set_fact:
        packets: "{{ interfaces['stdout'] | regex_findall('RX packets:([0-9]+)') }}"

    - name: sum all traff
      set_fact:
        summtrf: "{{ packets | map('int') | sum }}"

    - name: show results
      debug:
        msg: "{{ summtrf }}"

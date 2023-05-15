from desci.fetch import dpid

dpid_path = '46/data/exploring-lupus/output/data_lup.txt'

txtfile1 = dpid.fetch(dpid_path)
txtfile2 = dpid.fetch(dpid_path, options={'resolver': 'beta', 'cache': True})

print('dpid res least verbose: ', txtfile1)
print('dpid res: ', txtfile2)

'''

pip install editable .

'''


if __name__ == '__main__':

    from flowchem.client.client import get_all_flowchem_devices



    flowchem_devices = get_all_flowchem_devices()

    pump = flowchem_devices['my-plugin-device'].components['pump']
    valve = flowchem_devices['my-plugin-device'].components['valve']

    pump.put("infuse", params={"rate": "3", "volume": "4"})




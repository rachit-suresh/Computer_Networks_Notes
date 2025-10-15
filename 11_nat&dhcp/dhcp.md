# DHCP (Dynamic Host Configuration Protocol)

When a device joins a network, it needs an ip, so we can manually assign an ip(for a home network its alr but otherwise its a pain) but the dynamic one is what's used .

The device needs to know its ip, subnet mask, dns server config and the default gateway(ip of router) which is provided by dhcp in 4 steps

1. Discovery (Device broadcasts a DHCP discover message/packet when it joins a network that says give me an ip) - A device joins a network when you connect the laptop and a switch(assume a wired conn for now), atp router isnt even aware about this new device since it does not continuosly check the switch for a new device(it might in some certain circumstances), so the device itself broadcasts to all devices. The problem is that the device dosent have a src ip to broadcast so it sends the src as 0.0.0.0

 A network can have multiple DHCP servers(in home networks the router is the dhcp server)

2. Offer(All DHCP servers respond with an offer)

3. The device randomly chooses an offer as in the device broadcasts back saying this is the offer that i've chosen, only the chosen server takes things forward

4. Lease(Server gives ip on a lease from an ip pool) - DHCP servers dont permanently give out an ip since the device can always leave the network and make that ip redundant. ISP provides the range of ip it can use/pool to the router
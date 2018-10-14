from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from api.models import Snippet
from api.serializer import SnippetSerializer
from bin.powerstrip import Powerstrip
from bin.beamer import Beamer
from bin.hdmi_switch import HdmiSwitch
from bin.usb_switch import USBSwitch
import json

#renders api homepage
def view_api(request):
    return render(request, 'index_api.html', {})

#handles GET request for the beamer and shows all available functions
@api_view(['GET', 'POST'])		
def view_beamer(request):
    if request.user.is_staff:
        if request.method == 'GET':
            snippets = Snippet(classname='Beamer(usb, baudrate, bytesize, parity, stopbits, timeout)', code='on(input_on), off(input_off), changeState(input_change_state, input_on, input_off)')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
    else:
        return render(request, 'index_api.html', {})

#if GET request the function 'on' is shown, if POST request, the given data is read
#and the beamer is switched on
@api_view(['GET', 'POST'])		
def view_beamer_on(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='Beamer(usb, baudrate, bytesize, parity, stopbits, timeout)', code='on(input_on)')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            device = parsed_data[1].split(",")
            method = parsed_data[2]
            input_on = parsed_data[3]
            if name == "Beamer":
                if method == "on":
                    Beamer(device[0], int(device[1]), int(device[2]), device[3], int(device[4]), int(device[5])).on(bytes.fromhex(input_on))
                    print("device", device)
                    print(device[0], device[1], device[2], device[3], device[4], device[5])
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)
    

#if GET request the function 'off' is shown, if POST request, the given data is read
#and the beamer is switched off
@api_view(['GET', 'POST'])		
def view_beamer_off(request):
    
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='Beamer(usb, baudrate, bytesize, parity, stopbits, timeout)', code='off(input_off)')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            device = parsed_data[1].split(",")
            method = parsed_data[2]
            input_off = parsed_data[3]
            if name == "Beamer":
                if method == "off":
                    Beamer(device[0], int(device[1]), int(device[2]), device[3], int(device[4]), int(device[5])).off(bytes.fromhex(input_off))
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)
    

#if GET request the function 'change_state' is shown, if POST request, the given data is read
#and the beamer is switched on or off in dependence of the current status
@api_view(['GET', 'POST'])		
def view_beamer_change_state(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='Beamer(usb, baudrate, bytesize, parity, stopbits, timeout)', code='change_state(input_change_state, input_on, input_off))')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            device = parsed_data[1].split(",")
            method = parsed_data[2]
            input_change_state = parsed_data[3].split(",")
            if name == "Beamer":
                if method == "change_state":
                    Beamer(device[0], int(device[1]), int(device[2]), device[3], int(device[4]), int(device[5])).change_state(bytes.fromhex(input_change_state[0]),bytes.fromhex(input_change_state[1]), bytes.fromhex(input_change_state[2]))
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)
    

#handles GET request for the powerstrip and shows all available functions		
@api_view(['GET'])		
def view_powerstrip(request):
    if request.user.is_staff:
        if request.method == 'GET':
            snippets = Snippet(classname='Powerstrip(device_room)', code='switch_on(socket), switch_off(socket), switch_all_on(), switch_all_off(), status(socket), status_all()')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
    else:
        return render(request, 'index_api.html', {})

#if GET request the function 'switch_on' is shown, if POST request, the given data is read
#and the defined socket of the powerstrip is switched on
@api_view(['GET', 'POST'])		
def view_powerstrip_on(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='Powerstrip(device_room)', code='switch_on(socket)')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            device_room = parsed_data[1]
            method = parsed_data[2]
            socket = parsed_data[3]
            if name == "Powerstrip":
                if method == "switch_on":
                    Powerstrip(int(device_room)).switch_on(int(socket))
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)
    

#if GET request the function 'switch_off' is shown, if POST request, the given data is read
#and the defined socket of the powerstrip is switched off
@api_view(['GET', 'POST'])		
def view_powerstrip_off(request):
    if request.user.is_staff:
        if request.method == 'GET':
            snippets = Snippet(classname='Powerstrip(device_room)', code='switch_off(socket)')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            device_room = parsed_data[1]
            method = parsed_data[2]
            socket = parsed_data[3]
            if name == "Powerstrip":
                if method == "switch_off":
                    Powerstrip(int(device_room)).switch_off(int(socket))
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

#if GET request the function 'switch_all_on' is shown, if POST request, the given data is read
#and all sockets of the powerstrip are switched on
@api_view(['GET', 'POST'])		
def view_powerstrip_switch_all_on(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='Powerstrip(device_room)', code='switch_all_on()')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            device_room = parsed_data[1]
            method = parsed_data[2]
            if name == "Powerstrip":
                if method == "switch_all_on":
                    Powerstrip(int(device_room)).switch_all_on()
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

#if GET request the function 'switch_all_off' is shown, if POST request, the given data is read
#and all sockets of the powerstrip are switched off
@api_view(['GET', 'POST'])		
def view_powerstrip_switch_all_off(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='Powerstrip(device_room)', code='switch_all_off()')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            device_room = parsed_data[1]
            method = parsed_data[2]
            if name == "Powerstrip":
                if method == "switch_all_off":
                    Powerstrip(int(device_room)).switch_all_off()
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

#if GET request the function 'status' is shown, if POST request, the given data is read
#and the status of the defined socket of the powerstrip is returned
@api_view(['GET', 'POST'])		
def view_powerstrip_status(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='Powerstrip(device_room)', code='status(socket)')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            device_room = parsed_data[1]
            method = parsed_data[2]
            socket = parsed_data[3]
            if name == "Powerstrip":
                if method == "status":
                    Powerstrip(int(device_room)).status(int(socket))
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

#if GET request the function 'status_all' is shown, if POST request, the given data is read
#and the status of all sockets of the powerstrip are returned
@api_view(['GET', 'POST'])		
def view_powerstrip_status_all(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='Powerstrip(device_room)', code='status_all()')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            device_room = parsed_data[1]
            method = parsed_data[2]
            if name == "Powerstrip":
                if method == "status_all":
                    Powerstrip(int(device_room)).status_all()
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

#handles GET request for the hdmi_switch and shows all available functions
@api_view(['GET'])		
def view_hdmi_switch(request):
    if request.user.is_staff:
        if request.method == 'GET':
            snippets = Snippet(classname='HdmiSwitch()', code='status(), output_connections(output), get_connection(connection_feedback), status_in(), status_out(), get_in_out_devices(status), connect(inputs, output), switch_off(output), switch_on(output)')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
    else:
        return render(request, 'index_api.html', {})

# if GET request the function 'status' is shown, if POST request, the given data is read
# and the status of the switch is returned
@api_view(['GET', 'POST'])		
def view_hdmi_switch_status(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='HdmiSwitch()', code='status()')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            method = parsed_data[2]
            if name == "HdmiSwitch":
                if method == "status":
                    HdmiSwitch().status()
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

# if GET request the function 'output_connections' is shown, if POST request, the given data is read
# and the connections are returned
@api_view(['GET', 'POST'])		
def view_hdmi_switch_output_connections(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='HdmiSwitch()', code='output_connections(output)')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            method = parsed_data[2]
            output = parsed_data[3]
            if name == "HdmiSwitch":
                if method == "output_connections":
                    HdmiSwitch().output_connections(output)
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

# if GET request the function 'get_connection' is shown, if POST request, the given data is read
# and the connection is returned    
@api_view(['GET', 'POST'])		
def view_hdmi_switch_get_connection(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='HdmiSwitch()', code='get_connection(connection_feedback)')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            method = parsed_data[2]
            connection_feedback = parsed_data[3]
            if name == "HdmiSwitch":
                if method == "get_connection":
                    HdmiSwitch().get_connection(connection_feedback)
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

# if GET request the function 'status_in' is shown, if POST request, the given data is read
# and the status of all inputs are returned
@api_view(['GET', 'POST'])		
def view_hdmi_switch_status_in(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='HdmiSwitch()', code='status_in()')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            method = parsed_data[2]
            if name == "HdmiSwitch":
                if method == "status_in":
                    HdmiSwitch().status_in()
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

# if GET request the function 'status_out' is shown, if POST request, the given data is read
# and the status of all outputs are returned
@api_view(['GET', 'POST'])		
def view_hdmi_switch_status_out(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='HdmiSwitch()', code='status_out()')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            method = parsed_data[2]
            if name == "HdmiSwitch":
                if method == "status_out":
                    HdmiSwitch().status_out()
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

# if GET request the function 'get input and output devices' is shown, if POST request, the given data is read
# and the status of all are returned
@api_view(['GET', 'POST'])		
def view_hdmi_switch_get_in_out_devices(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='HdmiSwitch()', code='get_in_out_devices(status)')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            device_id = parsed_data[1]
            method = parsed_data[2]
            status = parsed_data[3]
            if name == "HdmiSwitch":
                if method == "get_in_out_devices":
                    HdmiSwitch().get_in_out_devices(status)
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)
  
# if GET request the function 'connect' is shown, if POST request, the given data is read
# and the given input and output will be connected 
@api_view(['GET', 'POST'])		
def view_hdmi_switch_connect(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='HdmiSwitch()', code='connect(inputs, output)')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            method = parsed_data[2]
            connect = parsed_data[3].split(",")
            if name == "HdmiSwitch":
                if method == "connect":
                    HdmiSwitch().connect(connect[0], connect[1])
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

# if GET request the function 'switch_off' is shown, if POST request, the given data is read
# and the given output is switched off
@api_view(['GET', 'POST'])		
def view_hdmi_switch_off(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='HdmiSwitch()', code='switch_off(output)')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            method = parsed_data[2]
            output = parsed_data[3]
            if name == "HdmiSwitch":
                if method == "switch_off":
                    HdmiSwitch().switch_off(output)
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

# if GET request the function 'switch_on' is shown, if POST request, the given data is read
# and the given output is switched on
@api_view(['GET', 'POST'])		
def view_hdmi_switch_on(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='HdmiSwitch()', code='switch_on(output)')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            method = parsed_data[2]
            output = parsed_data[3]
            if name == "HdmiSwitch":
                if method == "switch_on":
                    HdmiSwitch().switch_on(output)
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)
    
# handles GET request for the usb_switch and shows all available functions
@api_view(['GET'])		
def view_usb_switch(request):
    if request.user.is_staff:
        if request.method == 'GET':
            snippets = Snippet(classname='USBSwitch()', code='change_hub(), change_to_previous_hub(), change_to_number(hub), set_number_switch(), check_usb(), find_usb_switch()')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
    else:
        return render(request, 'index_api.html', {})

# if GET the function 'change_hub' is shown, if POST, it switches to the next output
@api_view(['GET', 'POST'])		
def view_usb_switch_change_hub(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='USBSwitch()', code='change_hub()')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            method = parsed_data[2]
            if name == "USBSwitch":
                if method == "change_hub":
                    USBSwitch().change_hub()
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

# if GET the function 'change_to_previous_hub' is shown, if POST, it switches to an output which is from the number smaller than the actual
@api_view(['GET', 'POST'])		
def view_usb_switch_change_to_previous_hub(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='USBSwitch()', code='change_to_previous_hub()')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            method = parsed_data[2]
            if name == "USBSwitch":
                if method == "change_to_previous_hub":
                    USBSwitch().change_to_previous_hub()
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

# if GET the function 'change_to_number' is shown, if POST, it switches to the given number of output
@api_view(['GET', 'POST'])		
def view_usb_switch_change_to_number(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='USBSwitch()', code='change_to_number(hub)')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            method = parsed_data[2]
            hub = parsed_data[3]
            if name == "USBSwitch":
                if method == "change_to_number":
                    USBSwitch().change_to_number(int(hub))
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

# if GET the function 'set_number_switch' is shown, if POST, the number of the output is set and count
@api_view(['GET', 'POST'])		
def view_usb_switch_set_number_switch(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='USBSwitch()', code='set_number_switch()')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            method = parsed_data[2]
            if name == "USBSwitch":
                if method == "set_number_switch":
                    USBSwitch().set_number_switch()
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

# if GET the function 'check_usb' is shown, if POST, it is controlled, if the usb switch is connected with the server  
@api_view(['GET', 'POST'])		
def view_usb_switch_check_usb(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='USBSwitch()', code='check_usb()')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            method = parsed_data[2]
            if name == "USBSwitch":
                if method == "check_usb":
                    USBSwitch().check_usb()
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

# for GET show function "find_usb_switch", if POST, the server is connected with the usb switch
@api_view(['GET', 'POST'])		
def view_usb_switch_find_usb_switch(request):
    if request.method == 'GET':
        if request.user.is_staff:
            snippets = Snippet(classname='USBSwitch()', code='find_usb_switch()')
            serializer = SnippetSerializer(snippets)
            return JsonResponse(serializer.data, safe=False)
        else:
            return render(request, 'index_api.html', {})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            parsed_data = encode_api_json(data)
            name = parsed_data[0]
            method = parsed_data[2]
            if name == "USBSwitch":
                if method == "find_usb_switch":
                    USBSwitch().find_usb_switch()
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer.errors, status=400)

# encode given json to classname, class parameters, function and function parameters
def encode_api_json(data):
    class_name = data['classname']
    code = data['code']
    name = class_name[0:class_name.find("(")]
    class_name.split(":")
    device = class_name[class_name.find("(")+1:class_name.find(")")] 
    method = code[0:code.find("(")]
    code.split(":")
    method_parameter = code[code.find("(")+1:code.find(")")]
    return (name, device, method, method_parameter)

from gravity_auto_exit.main import AutoExit

# left, upper, right, lower
# 2592*1944

if __name__ == '__main__':
    inst = AutoExit(  # 'http://172.16.6.176',
        'http://127.0.0.1',
        'admin',
        'Assa+123',
        debug=True,
        cam_port=83,
        resize_photo=(1100, 400, 2350, 1150),
        neurocore_login="admin",
        neurocore_password="admin"
    )
    # inst.set_post_request_url('http://127.0.0.1:8080/start_auto_exit')
    #inst.try_recognise_plate()
    inst.start()

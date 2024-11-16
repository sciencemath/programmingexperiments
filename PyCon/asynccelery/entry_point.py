from celery import group, chain

from banking import bank_deposit_money
from task_one import task_send_sms, task_send_whatsapp

"""
Needs Celery to run:
celery -A task_one worker --loglevel=INFO

pass in a --concurrency=# to instantiate multiple workers
(I have 9 cores so it defaults to nine without the flag)

--autoscale=1,10 (min,max)

-Q first,second,third (may want SMS, and WhatsApp) running different queues

celery -A task_one inspect active_queues
"""

def deposit_and_send_sms(account_no, amount, message, times):
    for i in range(times):
        bank_deposit_money(account_no, amount)
        
        # send SMS and WhatsApp
        sms_sent_status = task_send_sms.delay(account_no, message)
        whatsapp_sent_status = task_send_whatsapp.delay(account_no, message)
        
        print('SMS Status:', sms_sent_status.get())
        print('WhatsApp Status:', whatsapp_sent_status.get())
        
        
def trigger_delayed_notifications(account_no, amount, message):
    bank_deposit_money(account_no, amount)
    # send SMS and WhatsApp
    task_send_sms.apply_async((account_no, message), countdown=5)
    task_send_whatsapp.apply_async((account_no, message), countdown=5)

def deposit_and_send_sms_using_signature(account_no, amount, message):
    bank_deposit_money(account_no, amount)
    # create the signature <- template invocation (partial functions)
    sig_sms = task_send_sms.si(account_no, message)
    # apply signature
    sms_sent_status = sig_sms.delay()
    # alternatively
    sms_sent_status = sig_sms.apply_async()
    sms_sent_status = sig_sms.apply_async(countdown=5)
    
def deposit_and_send_sms_whatsapp_using_group():
    bank_deposit_money(1234, 5000)
    sig_sms = task_send_sms.si(1234, 'Your account has been credited with $5000')
    sig_whatsapp = task_send_whatsapp.si(1234, 'Your account has been credited with $5000')
    
    grp = group(sig_sms, sig_whatsapp)
    
    result = grp.delay()
    # or
    # grp.apply_async()
    print('Group results: ', result.get())
    
def send_sms_and_whatsapp_using_chain(account_no, amount, message):
    sig_sms = task_send_sms.signature((account_no, message))
    sig_whatsapp = task_send_whatsapp.signature((account_no, message))
    result = chain(sig_sms, sig_whatsapp).delay()
    # or result = chain(sig_sms, sig_whatsapp).apply_async()
    print(result.get())
    
# def call_bounded_task():
#     bounded_task.delay(('Mathias', 'King'), kwargs={'confname': 'pycon', 'place': 'pittsburgh'})

def put_task_in_fist_queue():
    result = task_send_sms.apply_async((12345, 'USD $5000 Deposited'), queue='first')
    result.get()

def put_task_in_second_queue():
    result = task_send_whatsapp.apply_async((12345, 'USD $5000 Deposited'), queue='second')
    result.get()
    
if __name__ == '__main__':
    put_task_in_fist_queue()
    put_task_in_second_queue()
    #first_task().delay()
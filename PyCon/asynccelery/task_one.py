from celery import Celery

# Celery uses RabbitMQ, this is my docker instance
# To use Redis just docker install and change broker and backend
app = Celery('task_one', backend='rpc://', broker='pyamqp://guest:guest@localhost//')

app.conf.task_default_queue = 'first'

@app.task
def task_send_sms(account_no, message):
    print("Sending SMS to account holder of {0} with message \n\n {1}".format(account_no, message))
    #return 'SMS Sent Successfully!'
    return True
    
@app.task
def task_send_whatsapp(account_no, message):
    #print("When using chain() SMS Sent Status is {0}".format(sms_sent_status))
    print('Sending WhatsApp to account holder of {0} with message \n\n {1}'.format(account_no, message))
    return 'WhatsApp Message Sent Successfully!'

# @app.task(bind=True)
# def bounded_task(self, *args, **kwargs):
#     print('>>>>>>>>>>>>>-------------->>>>>>>>>>>>>')
#     # task id
#     print('Task ID: {0}'.format(self.request.id))
#     # task name
#     print('Task Name: {0}'.format(self.name))
#     # task args
#     print('Task args: {0}'.format(self.request.args))
#     # task kwargs
#     print('Task kwargs: {0}'.format(self.request.kwargs))
#     # task status
#     print('Task Status: {0}'.format(self.AsyncResult(self.request.id).state))

@app.task(queue='first')
def first_task():
    print("First Task Queue")
    return "First Task Done!"
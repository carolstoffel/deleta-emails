import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import re
import sys

lista_negra = ['news@mkt.americanas.com',
               'news@emkt.submarino.com.br',
               'passageiro@99app.com',
               'privacidade@betrybe.com',
               'verify@twitter.com',
               'comunicacao.bbg@unemat.br',
               'no-reply@picpay.com',
               'luciana.lima@igti.edu.br',
               'no-reply@accounts.google.com',
               'reply@t.mail.coursera.org',
               'reply@spotify.com',
               'mobly@novidades.mobly.com.br',
               'info@news.runtastic.com',
               'udemy@email.udemy.com',
               'viniciusdpace@yahoo.com.br',
               'hello@promos.memrise.com',
               'uber.brasil@uber.com',
               'no-reply@e.udemymail.com',
               'mobly@novidades.mobly.com.br',
               'lojavirtual@biofase.com.br',
               'shop@bpe.mail.givingassistant.org',
               'info@txt.galiwer.com',
               'casasbahia-recomenda@shoptarget.com.br',
               'info@news.gedozec.com',
               'marketing@biofase.com',
               'info@infor.kanvaser.com',
               'comunicado18587691@esfera.com',
               'gisneile@ig.com.br',
               'info@say.outbrin.com',
               'VWEvEsX47C8s@davidlabrousse.com',
               'info@promo.transferlp.com',
               'aliexpress@notice.aliexpress.com',
               'atendimento@mc.meliuz.com.br',
               'latam@mail.latam.com',
               'python-announce-list@python.org',
               'udemy@email.udemy.com',
               'noreply@comunicacao.bancointer.com.br',
               'no-reply@m.mail.coursera.org',
               'fastnews@relacionamento.fastshop.com.br',
               'ancestry@email.ancestry.com',
               'invitations@linkedin.com'
               ]
def create_log(lista):
    with open('lista_de_emails.txt', 'a') as arquivo:
        for email in lista:
            arquivo.write(email+',')


# account credentials
username = "DIGITE SEU EMAIL AQUI"
password = "DIGITE SUA SENHA AQUI"


# create an IMAP4 class with SSL
imap = imaplib.IMAP4_SSL("imap.gmail.com")

# authenticate
imap.login(username, password)

status, messages = imap.select() # inbox
#status, messages = imap.select('"[Gmail]/Spam"') # spam
#status, messages = imap.select('All')

# number of top emails to fetch
N = 1000000 # number of messages
# total number of emails
messages = int(messages[0])

from_email_ = []
try:
    for i in range(messages, messages-N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode()
                # email sender
                from_ = msg.get("From")
                #print("Subject:", subject)
                #print("From:", from_)
                from_email_.append(re.findall(r'<([^ ]*)>', from_)[0]) # [0] faz com que seja anexado em forma de string ao inves de lista
                from_email_2 = re.findall(r'<([^ ]*)>', from_)[0]
                #print(from_email_2)
                if from_email_2 in lista_negra:
                    print('Excluindo email: ',from_email_2)
                    imap.store(str(i), '+X-GM-LABELS', r'\Trash')
                    print('Email do rementente', from_email_2, 'excluído.')
except OSError as err:
    print("OS error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
finally:
    imap.expunge()
    imap.close()
    imap.logout()
    create_log(from_email_)

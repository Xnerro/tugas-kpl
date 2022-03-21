from flask import Flask, redirect,  render_template, request, session
from flask_wtf import Form
from wtforms import *
from wtforms.validators import DataRequired
import pymongo

class form(Form):
    nik = StringField('nik', [DataRequired()] )
    nama = StringField('nama', [DataRequired()])
    jenis_kelamin = RadioField('jenis_kelamin', choices=[('Laki-laki', u'Laki-laki'), ('Perempuan', u'Perempuan')])
    golongan = RadioField('golongan', choices=[('1', u'I'), ('2', u'II'), ('3', u'III'), ('4', u'IV')])
    gapok = IntegerField('gapok', [DataRequired()])
    tunjangan = IntegerField('tunjangan', [DataRequired()])
    potongan = IntegerField('potongan', [DataRequired()])
    submit = SubmitField()

class pegawai(object):
    Database = None

    def data(nik, nama, jns_kelamin, Golongan, Gapok, tunjanagan, potongan):
        pegawai.Database['sample'].update_one(
            {'_id' : 'item_id'},
            {'$inc': {'seq_name' : 1}
        })

        x = pegawai.getid()
        total = (Gapok + tunjanagan) - potongan
        data = {
            '_id'   : x['seq_name'],
            'nik'   : nik,
            'nama'  : nama,
            'jenis_kelamin'  : jns_kelamin,
            'golongan'  : Golongan,
            'gapok'  : Gapok,
            'tunjangan'  : tunjanagan,
            'potongan' : potongan,
            'total'  : total,
        }
        return data

    @staticmethod
    def initialize():
        client = pymongo.MongoClient("mongodb+srv://root:dadasdudus12@cluster0.wc2gb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        pegawai.Database = client['test']
        

    @staticmethod
    def tambah(data):
        pegawai.Database['pegawai'].insert_one(data)

    @staticmethod
    def update(nik, nama, jns_kelamin, Golongan, Gapok, tunjanagan, potongan):
        total = (Gapok+tunjanagan) - potongan
        pegawai.Database['pegawai'].update_one(
        {"nik": nik},
        {"$set": {"nik": nik, 'nama' : nama, 'jenis_kelamin' : jns_kelamin, 'golongan' : Golongan, 'gapok' : Gapok, 'tunjangan' : tunjanagan, 'potongan' : potongan, 'total' : total}}
        )   
    
    def getgolongan(golongan):
        if golongan == '1':
            return 2000
        elif golongan == '2':
            return 3000
        elif golongan == '3':
            return 4000
        elif golongan == '4':
            return 5000
        else: return 0

    def getid():
        return pegawai.Database['sample'].find_one({})
    
    def getnik(nik):
        return pegawai.Database['pegawai'].find_one({'nik' : nik})

    def getall():
        return pegawai.Database['pegawai'].find({})


pegawai.initialize()


app = Flask(__name__)
app.secret_key = 'sdassd'


@app.route('/insert', methods=['GET', 'POST'])
def home():
    pform = form()
    if request.method == 'POST':
        nik = request.form['nik']
        nama = request.form['nama']
        jenis_kelasmin = request.form['jenis_kelamin']
        golongan = request.form['golongan']
        tunjangan = int(request.form['tunjangan'])
        potongan = int(request.form['potongan'])
        data = pegawai.data(nik, nama, jenis_kelasmin, golongan, pegawai.getgolongan(golongan), tunjangan, potongan)
        pegawai.tambah(data)
        return f'<h1>Input Success</h1> <a href="/">data</a>'
    else:
        return render_template('index.html', form = pform)

@app.route('/', methods=['GET', 'POST'])
def data():
    pform = form()
    if request.method == 'POST':
        if request.form['button'] == 'delete':
            nik = request.form['nik']
            pegawai.Database['pegawai'].delete_one({'nik' : nik})
            data = pegawai.getall()
            # nik = request.form['nik']
            # session['id'] = nik
            # session['status'] = 'delete'
            return f'<h1>Input Success</h1> <a href="/">data</a>'
        elif request.form['button'] == 'edit':
            nik = request.form['nik']
            session['id'] = nik
            session['status'] = 'update'
            return redirect('/update')
    else:
        x = pegawai.getall()
        return render_template('data.html', data = x, form = pform)
    x = pegawai.getall()
    return render_template('data.html', data = x, form = pform)

@app.route('/update', methods = ['POST', 'GET'])
def update():
    pform = form()
    data = pegawai.Database['pegawai'].find_one({'nik' : session['id']})
    pform.nik.data = data['nik']
    pform.nama.data = data['nama']
    pform.jenis_kelamin.data = data['jenis_kelamin']
    pform.golongan.data = data['golongan']
    pform.gapok.data = data['gapok']
    pform.tunjangan.data = data['tunjangan']
    pform.potongan.data = data['potongan']
    if request.method == 'POST':
        dataF = request.form
        session.pop('status')
        session.pop('id')
        pegawai.update(dataF['nik'], dataF['nama'], dataF['jenis_kelamin'], dataF['golongan'], pegawai.getgolongan(dataF['golongan']), int(dataF['tunjangan']), int(dataF['potongan']))
        return f'<h1>Input Success</h1> <a href="/">data</a>'
    return render_template('update.html', form = pform)

if '__main__' == __name__:
    app.run(debug=True)
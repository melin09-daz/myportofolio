Nama : Amelinda Fedora Faragusti

NPM : 2506540475

Kelas : PBP F

## Deskripsi Proyek 

Website ini merupakan portofolio pribadi yang dibuat untuk menampilkan profil diri dan sejauh ini baru menambahkan skill saja, namun ke depannya akan terus dikembangkan. Proyek ini dikerjakan sebagai tugas individu untuk mata kuliah PBP (Pemrograman Berbasis Platform), Semester Gasal 2026/2027.

## Proses Mingguan

Week 1: Setup awal Django beserta template portofolio.

Week 2: Menambahkan section baru yaitu skill serta tampilan yang sedikit diubah.

Week 3: Implementasi MVT di Experience dan Project

Week 4: Form & Data Delivery di Experience dan Project

### Tugas 1 

1. Iya, saya menggunakan elemen semantik HTML5 salah satunya adalah &lt;section> yang dimana dapat membantu saya untuk membagi bagian-bagian fungsional halaman (seperti bagian Hero/Profil) dan pengguna dapat lebih mudah untuk navigasi ke bagian yang mereka inginkan.

2. Salah satu tantangan yang saya hadapi adalah pada tampilan desktop, layout profil (hero section) menggunakan format 2 kolom menyamping: kolom foto diri di satu sisi dan deskripsi, kotak info (NPM/Program), tombol aksi, serta tautan sosial di sisi lain. Saat berpindah ke layar ponsel yang sempit, mempertahankan tata letak menyamping membuat teks terhimpit dan foto menjadi terlalu kecil. Oleh karena itu, flex-direction atau grid harus diubah menjadi vertikal (flex-direction: column) dengan urutan elemen yang tetap logis dan proporsional. Salah satu evaluasi yang saya lakukan adalah penggunaan clamp yang dimana melalui parameter minimum di clamp(), browser otomatis menahan ukuran judul agar pas di dalam kontainer mobile tanpa memecah kata secara berlebihan.

3. Karena masih hanya mengandalkan HTML dan CSS, masih belum bisa mengembangkan website dengan lebih kompleks dan variatif. Pada proyek selanjutnya mungkin bisa ditambahkan dengan bahasa lainnya seperti javascript dan ditambah dengan section section lainnya agar isi portofolio lebih menarik.

Dalam mengerjakan proyek ini, saya sama sekali tidak menggunakan bantuan AI. Kebanyakan saya melihat tutorial dari youtube dengan banyaknya variasi yang ada untuk ide ide isi dalam portofolio. Jika masih ada code yang dibingungkan dapat melihat source yang ada di google. 

### Tugas 2

1. Pada saat membuka halaman protofolio baru di browser (misalnya https://.../project/ atau https://.../experience/), Django memproses permintaan tersebut melalui siklus MVT (Model View Template). Alur prosesnya:
- Browser user mengirim HTTP GET Request ke server.
- Membaca domain utama, mengarahkan rute ke modul aplikasi (urls.py Proyek (portofolio/urls.py)).
- Mencocokan endpoint ('project/') dengan fungsi View (urls.py Aplikasi (main/urls.py)).
- Meminta data ke Model (models.py ke Database SQLite).
- Mengembalikan data objek/query.
- Mengemas data ke dalam Dictionary (Context) lalu memanggil Template.
- Django Template Engine (DTE) memasukkan data ke HTML (Template HTML (templates/project.html)).
- Menghasilkan HTTP Response utuh (HTML, CSS, dan Gambar) (views.py)
- Broswer user menerima kode HTML dan merender halaman visual kepada pengguna.

Peran masing-masing komponen dalam proyek:
- urls.py Proyek (portofolio/urls.py) : Ketika permintaan HTTP masuk, memeriksa awalan URL dan menggunakan fungsi include() untuk meneruskan rute tersebut ke urls.py milik main.
- urls.py Aplikasi (main/urls.py) : Mencocokkan path URL yang diminta (contoh: '' untuk halaman utama, 'experience/' untuk pengalaman, atau 'project/' untuk proyek) dengan fungsi controller yang ada di views.py.
- views.py : Menerima objek request dari browser, memiliki hubungan dengan models.py untuk mengambil data yang dibutuhkan dari database, mengumpulkan data ke dalam sebuah kamus Python yang disebut context (contoh: {'name': '...', 'project_list': project_list}), serta memanggil fungsi render() untuk menggabungkan data konteks dengan template HTML yang sesuai.
- models.py : mendefinisikan struktur, tipe data, serta aturan dari data yang disimpan (contoh: atribut title, description, category, tech_stack, repository_url).
- template : Template menerima data dari view, menyusunnya ke dalam kerangka web yang sudah di styling dengan CSS/gambar, dan menghasilkan halaman web yang siap diakses oleh browser pengguna.

2. Jika di Template (Hardcoded), setiap kali ingin menambah pengalaman, memperbaiki typo judul proyek, atau mengganti link GitHub, developer harus membuka file HTML, mencari baris kode yang tepat di antara ratusan tag <div>, lalu melakukan commit dan deploy ulang aplikasi. Akibatnya, dapat merusak struktur tag HTML atau tata letak CSS. Dengan menggunakan Model, data terpisah dari tampilan. Kita cukup menambahkan atau mengedit data melalui Django Admin (/admin) atau Django Shell di terminal tanpa mengubah satu baris pun kode HTML. Struktur antarmuka tetap aman dan bebas dari risiko broken layout.

3. Perbedaan antara perintah makemigrations dan migrate pada Django:
yang diperiksa:
- python manage.py makemigrations: Membandingkan kode di models.py saat ini dengan berkas migrasi sebelumnya.
- python manage.py migrate: Memeriksa berkas migrasi mana yang belum pernah dicatat pada tabel django_migrations di database.

Output / Hasil:
- python manage.py makemigrations: Berkas Python baru di folder migrations/ (contoh: 0003_add_field_xyz.py).
- python manage.py migrate: Perubahan tabel, kolom, atau relasi langsung pada mesin database (SQLite, PostgreSQL, MySQL, dll.).

Hubungan dengan Database:
- python manage.py makemigrations: Belum menyentuh database sama sekali.
- python manage.py migrate: Mengubah skema database secara langsung (menjalankan perintah SQL seperti CREATE TABLE, ALTER TABLE, dll.).

Keduanya harus dijalankan berurutan ketika kita mengubah struktur class di models.py:
- python manage.py makemigrations (merekam perubahan ke berkas migrasi).
- python manage.py migrate (menerapkan berkas migrasi tersebut ke database).

Contoh:
```python
# main/models.py
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50)
    repository_url = models.URLField(blank=True, null=True)
```
Ketika kita membuat class model Project baru dari awal:
- makemigrations: Mencatat operasi CreateModel(name='Project', fields=...) ke berkas 0004_project.py.
- migrate: Menjalankan SQL CREATE TABLE main_project (...) di dalam database. 
Tanpa perintah ini, akan terjadi error ketika view mencoba mengambil data dari model Project.

### Tugas 3

1. Mengapa menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual? Untuk menghemat waktu karena field form HTML dan tipe datanya dibuat otomatis mengikuti definisi pada Model. Pada fungsi form.is_valid() otomatis mengecek format data serta mencegah data berbahaya masuk ke database. Penyimpanan database juga lebhi praktis dengan memanggil form.save() untuk menyimpan data ke database tanpa perlu membuat satu per satu secara manual. 

Mengapa diwajibkan menambahkan {% csrf_token %} pada form tersebut? Tag {% csrf_token %} wajib digunakan pada metode ubah data yang sudah dibuat untuk mencegah serangan CSRF(Cross-Site Request Forgery). Django otomatis memblokir dengan pesan 403 Forbidden, sehingga database tetap aman.

2. Saat ini, JSON lebih disukai dibandingkan XML pada aplikasi modern (terutama pada arsitektur RESTful API) karena ukurannya yang lebih ringkas, parser yang sangat cepat, dan integrasi yang sangat natural dengan JavaScript di sisi frontend.

3. Alur yang terjadi saat menggunakan fungsi view untuk mengembalikan data portofolio dalam bentuk JSON:
- HTTP Request: mengirimkan request HTTP GET ke URL (contoh: /api/projects/).
- Routing URL (urls.py): Django mencocokan URL dan meneruskan permintaan ke fungsi view terkait.
- Pengambilan data dari database (querying): Hasil operasi ini menghasilkan sekumpulan objek Python berupa QuerySet.
- Serialisasi data: QuerySet diubah dari objek Python ke bentuk string berformat JSON.
- HTTP Response: Data JSON dikemas dengan menggunakan return HttpResponse(serialized_data, content_type="application/json").
- Django mengirimkan respon HTTP tersebut kembali ke user. Browser menerima dan langsung parsing sehingga dapat langsung ditampilkan di layar.

Mengapa perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan? HTTP hanya mengirimkan teks dasar. Objek Model/QuerySet Django terlalu kompleks dan menganduk tipe data yang tidak bisa dibaca langsung oleh JSON tanpa diubah ke tipe data standar. Jadi, serialization bertugas menerjemahkan tipe data kompleks tersebut ke dalam tipe data yang valid di JSON (seperti string, number, boolean, atau array).
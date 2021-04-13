>Last update Mon Apr 12, 2021

The Bodyport system must be able to upload a measurement within a reasonable amount of time. A key factor is file size - more specifically the file size of the raw signal. Therefore, the software goals are: <br />
- Support local directory file upload and basic CRUD operations of file <br />
- Compress selected file using Huffman coding algorithm <br />
- Display compression analysis <br />

# Project structure
**bodyport-assessment/ <br/>**
&nbsp;  app.py: Application starting point <br/>
&nbsp;  doc/ Contains software design document <br/>

# Build
pip install -r requirements.txt
>Activate virtual environment <br/>
>source ./env/bin/activate <br/>

### Create db
From python3 terminal
<code>
>python3 <br/>
> from app import db <br/>
> db.create_all() <br/>
> db.session.commit() <br/>
> exit() <br/>
</code>

### Start application
<code>
python3 app.py
</code>

# Compression schema
Once a file is selected, the application will use **binascii** library to read the content of the binary file and store it as 'data' in the **BinaryFile** object to be saved as BLOB type to the sql table. The relational **SQLAlchemy** library is used because of ease of implementation and the inherit relational property between files. At the moment, the application only supports uploading file from the same directory, if there is no file found no new row will be inserted. <br />

A user can view the uploaded files and select `compress` option to initiate Huffman encoding of the BLOB string. Huffman algorithm will calculate the frequency table and build the encoded tree. Once finishes, the application will store the new compressed file and redirect the user to the analysis page. <br />

I have been researching [this](https://www.programiz.com/dsa/huffman-coding) to implement the compression engine.

# Future improvements
1. Finish the Huffman encoding and decoding algorithm
2. Support file uploading other than local directory




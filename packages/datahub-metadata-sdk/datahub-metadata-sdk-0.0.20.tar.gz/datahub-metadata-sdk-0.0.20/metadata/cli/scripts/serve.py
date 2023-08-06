import sys
import pandas
import os.path
import streamlit as st
from functools import partial

from metadata import get_current_context
from metadata.utils.format import sizeof_fmt

urn = sys.argv[1]

context = get_current_context()
client = context.client 
ds = client.get_dataset(urn)

st.header(f'{ds.display_name}')

st.caption('Urn')
st.text(ds.urn)

if ds.description:
    st.caption('Description')
    st.write(ds.description)

if ds.owners:
    st.caption('Owners')
    st.text(', '.join(ds.owners))

if ds.properties:
    st.caption('Properties')
    properties = [(key, value) for key, value in ds.properties.items()]
    df = pandas.DataFrame(properties, columns=["Name", "Value"])
    st.table(df)


@st.cache
def get_artifacts(uri):
    context = get_current_context()
    storage_client = context.storage_client
    files = storage_client.list(uri, recursive=True)
    return [(file[len(ds.uri)+1:], sizeof_fmt(storage_client.get_meta(file)['contentLength']))
        for file in files
    ]

st.caption('Contents')
query = st.text_input('Filter')
items = get_artifacts(ds.uri)
total_count = len(items)
items = [e for e in items if query in e[0]]
current_count = len(items)

st.caption(f'{current_count} / {total_count}')

selected = []
for name, size in items:
    if st.checkbox(f'{name} [size={size}]'):
        selected.append(name)

def progress_callback(bar, percent):
    bar.progress(int(percent * 100))

dest = st.text_input('Target Path', value=os.path.abspath(os.path.curdir))
if selected:
    if st.button('Download'):
        storage_client = context.storage_client

        with st.spinner('Wait for it...'):
            for name in selected:
                x = st.container()
                x.info(f'Downloading {name}')
                bar = st.progress(0)
                target = os.path.abspath(os.path.join(dest, name))
                storage_client.download(os.path.join(ds.uri, name),
                    target, progress_callback=partial(progress_callback, bar))
                bar.progress(100)
                x.empty()
                x.success(f'Downloaded {name}')
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import torch
from PIL import Image as PILImage
import cv2
import towhee
from image_utils import get_model, preprocess

dim = 2560
torch_model = get_model()


def efficientnet_b7(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = PILImage.fromarray(img.astype('uint8'), 'RGB')
    img = torch.unsqueeze(preprocess(img), 0)
    img = img.to('cuda' if torch.cuda.is_available() else 'cpu')
    embedding = torch_model(img).detach().cpu().numpy()
    return embedding.reshape([dim])


def get_milvus_collection(path_list, collection_name, rebuild=False):
    id_path_list = [(idx, path) for idx, path in enumerate(path_list)]
    connections.connect(host='127.0.0.1', port='19530')
    if rebuild:
        utility.drop_collection(collection_name)
    else:
        if utility.has_collection(collection_name):
            return Collection(collection_name), dict(id_path_list)
        else:
            print("Collection not exist, rebuild it.")

    fields = [
        FieldSchema(name='id',
                    dtype=DataType.INT64,
                    descrition='ids',
                    is_primary=True,
                    auto_id=False),
        # FieldSchema(name='path', dtype=DataType.VARCHAR, descrition='pathes'),
        FieldSchema(name='embedding',
                    dtype=DataType.FLOAT_VECTOR,
                    descrition='embedding vectors',
                    dim=dim)
    ]
    schema = CollectionSchema(fields=fields, description='deduplication image search')
    collection = Collection(name=collection_name, schema=schema)

    # create IVF_FLAT index for collection.
    index_params = {
        'metric_type': 'L2',
        'index_type': "IVF_FLAT",
        'params': {"nlist": 2048}
    }
    collection.create_index(field_name="embedding", index_params=index_params)

    (
        towhee.dc['id', 'path'](id_path_list)
        .runas_op['id', 'id'](func=lambda x: int(x))
        .image_decode['path', 'img']()
        .runas_op['img', 'vec'](func=efficientnet_b7)
        .tensor_normalize['vec', 'vec']()
        .to_milvus['id', 'vec'](collection=collection, batch=100)
    )
    return collection, dict(id_path_list)

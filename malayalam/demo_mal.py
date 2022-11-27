import torch
from torch.autograd import Variable
from malayalam import utils
from malayalam import dataset
from PIL import Image
import torch
from PIL import Image
import torch
from torch.autograd import Variable
from PIL import Image
import malayalam.models.crnn as crnn

def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)

def testeval(img_path, model, converter):
 
    transformer = dataset.resizeNormalize((100, 32))
    image = Image.open(img_path).convert('L')
    image = transformer(image)
    if torch.cuda.is_available():
        image = image.cuda()

    image = image.view(1, *image.size())
    image = Variable(image)

    model.eval()
    preds = model(image)

    _, preds = preds.max(2)
    preds = preds.squeeze(1)
  
    preds_size = Variable(torch.LongTensor([preds.size(0)]))
    sim_pred = converter.decode(preds.data, preds_size.data, raw=False)

    return sim_pred

def predict(img_path):
    lexicon_filename = "malayalam/chars.txt"
    p = open(lexicon_filename, 'r').readlines()
    alphabet = p
    converter = utils.strLabelConverter(alphabet)

    nclass = len(p)
    model_path='malayalam/mal_crnn.pth'
    model = crnn.CRNN(32, 1, nclass, 256)
    model.apply(weights_init)
    model_dict = model.state_dict()
    checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
    for key in list(checkpoint.keys()):
        if 'module.' in key:
            checkpoint[key.replace('module.', '')] = checkpoint[key]
            del checkpoint[key]

    model_dict.update(checkpoint)
    model.load_state_dict(checkpoint)

    pred = testeval(img_path, model, converter)
    pred = pred.strip()
    return pred

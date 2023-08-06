# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nlhappy',
 'nlhappy.algorithms',
 'nlhappy.callbacks',
 'nlhappy.configs',
 'nlhappy.data',
 'nlhappy.datamodules',
 'nlhappy.layers',
 'nlhappy.layers.attention',
 'nlhappy.layers.classifier',
 'nlhappy.layers.embedding',
 'nlhappy.metrics',
 'nlhappy.models',
 'nlhappy.models.entity_extraction',
 'nlhappy.models.event_extraction',
 'nlhappy.models.prompt_relation_extraction',
 'nlhappy.models.question_answering',
 'nlhappy.models.relation_extraction',
 'nlhappy.models.span_extraction',
 'nlhappy.models.text_classification',
 'nlhappy.models.text_multi_classification',
 'nlhappy.models.text_pair_classification',
 'nlhappy.models.text_pair_regression',
 'nlhappy.models.token_classification',
 'nlhappy.tricks',
 'nlhappy.utils']

package_data = \
{'': ['*'],
 'nlhappy.configs': ['callbacks/*',
                     'datamodule/*',
                     'log_dir/*',
                     'logger/*',
                     'model/*',
                     'trainer/*']}

install_requires = \
['datasets>=2.0.0',
 'hydra-colorlog>=1.1.0',
 'hydra-core==1.1',
 'pydantic==1.10.2',
 'pytorch-lightning>=1.6.5',
 'rich>=12.4.3,<13.0.0',
 'srsly>=2.4.5',
 'torch>=1.8.0',
 'transformers>=4.17.0']

extras_require = \
{':extra == "all"': ['googletrans==4.0.0rc1', 'wandb>=0.12.18']}

entry_points = \
{'console_scripts': ['nlhappy = nlhappy.run:train']}

setup_kwargs = {
    'name': 'nlhappy',
    'version': '2022.12.12',
    'description': '自然语言处理(NLP)',
    'long_description': '\n<div align=\'center\'>\n\n# NLHappy\n<a href="https://pytorch.org/get-started/locally/"><img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-ee4c2c?logo=pytorch&logoColor=white"></a>\n<a href="https://pytorchlightning.ai/"><img alt="Lightning" src="https://img.shields.io/badge/-Lightning-792ee5?logo=pytorchlightning&logoColor=white"></a>\n<a href="https://hydra.cc/"><img alt="Config: Hydra" src="https://img.shields.io/badge/Config-Hydra-89b8cd"></a>\n<a href="https://github.com/ashleve/lightning-hydra-template"><img alt="Template" src="https://img.shields.io/badge/-Lightning--Hydra--Template-017F2F?style=flat&logo=github&labelColor=gray"></a>\n<a href="https://spacy.io/"><img alt="Spacy" src="https://img.shields.io/badge/component-%20Spacy-blue"></a>\n<a href="https://wandb.ai/"><img alt="WanDB" src="https://img.shields.io/badge/Log-WanDB-brightgreen"></a>\n</div>\n<br><br>\n\n## 📌&nbsp;&nbsp; 简介\n\nnlhappy致力于快速完成NLP任务,你唯一需要做的就是将数据处理为任务对应的数据类.\n> 它主要的依赖有\n- [transformers](https://huggingface.co/docs/transformers/index): 下载预训练权重\n- [pytorch-lightning](https://pytorch-lightning.readthedocs.io/en/latest/): 模型训练\n- [datasets](https://huggingface.co/docs/datasets/index): 构建数据集\n- [pydantic](https://wandb.ai/): 构建数据模型\n\n\n## 🚀&nbsp;&nbsp; 安装\n<details>\n<summary><b>安装nlhappy</b></summary>\n\n> 推荐先去[pytorch官网](https://pytorch.org/get-started/locally/)安装pytorch和对应cuda\n```bash\n# pip 安装\npip install --upgrade pip\npip install --upgrade nlhappy\n```\n</details>\n\n<details>\n<summary><b>其他可选</b></summary>\n\n> 推荐安装wandb用于可视化训练日志\n- 注册: https://wandb.ai/\n- 获取认证: https://wandb.ai/authorize\n- 登陆:\n```bash\nwandb login\n```\n模型训练开始后去[官网](https://wandb.ai/)查看训练实况\n</details>\n\n\n\n\n## ⚡&nbsp;&nbsp; 开始任务\n\n<details>\n<summary><b>文本分类</b></summary>\n\n> 数据处理\n```python\nfrom nlhappy.utils.make_doc import Doc, DocBin\nfrom nlhappy.utils.make_dataset import DatasetDict\n# 构建corpus\n# 将数据处理为统一的Doc对象,它存储着所有标签数据\ndocs = []\n# data为你自己的数据\n# doc._.label 为文本的标签,之所以加\'_\'是因为这是spacy Doc保存用户自己数据的用法\nfor d in data:\n    doc = nlp(d[\'text\'])\n    doc._.label = d[\'label\']\n    docs.append(doc)\n# 保存corpus,方便后边badcase分析\ndb = DocBin(docs=docs, store_user_data=True)\n# 新闻文本-Tag3为保存格式目录,需要更换为自己的形式\ndb.to_disk(\'corpus/TNEWS-Tag15/train.spacy\')\n# 构建数据集,为了训练模型\nds = convert_docs_to_tc_dataset(docs=docs)\n# 你可以将数据集转换为dataframe进行各种分析,比如获取文本最大长度\ndf = ds.to_pandas()\nmax_length = df[\'text\'].str.len().max()\n# 数据集切分\ndsd = train_val_split(ds, val_frac=0.2)\n# 保存数据集,注意要保存到datasets/目录下\ndsd.save_to_disk(\'datasets/TNEWS\')\n```\n> 训练模型\n\n- 编写训练脚本,scripts/train.sh\n```\nnlhappy \\\ndatamodule=text_classification \\\ndatamodule.dataset=TNEWS \\\ndatamodule.plm=hfl/chinese-roberta-wwm-ext \\\ndatamodule.batch_size=32 \\\nmodel=bert_tc \\\nmodel.lr=3e-5 \\\nseed=1234\n# 默认为单gpu 0号显卡训练,可以通过以下方式修改显卡\n# trainer.devices=[1]\n# 单卡半精度训练\n# trainer.precision=16\n# 使用wandb记录日志\n# logger=wandb\n# 多卡训练\n# trainer=ddp trainer.devices=4\n```\n\n- 后台训练\n```\nnohup bash scripts/train.sh >/dev/null 2>&1 &\n```\n- 如果设置logger=wandb则现在可以去[wandb官网](https://wandb.ai/)查看训练详情了, 并且会自动产生logs目录里面包含了训练的ckpt,日志等信息.\n\n> 构建自然语言处理流程,并添加组件\n```python\nimport nlhappy\n\nnlp = nlhappy.nlp()\n# 默认device cpu, 阈值0.8\nconfig = {\'device\':\'cuda:0\', \'threshold\':0.9}\ntc = nlp.add_pipe(\'text_classifier\', config=config)\n# logs文件夹里面训练的模型路径\nckpt = \'logs/experiments/runs/TNEWS/date/checkpoints/epoch_score.ckpt/\'\ntc.init_model(ckpt)\ntext = \'文本\'\ndoc = nlp(text)\n# 查看结果\nprint(doc.text, doc._.label, doc.cats)\n# 保存整个流程\nnlp.to_disk(\'path/nlp\')\n# 加载\nnlp = nlhappy.load(\'path/nlp\')\n```\n> badcase分析\n```python\nimport nlhappy\nfrom nlhappy.utils.make_doc import get_docs_form_docbin\nfrom nlhappy.utils.analysis_doc import analysis_text_badcase, Example\n\ntargs = get_docs_from_docbin(\'corpus/TNEWS-Tag15/train.spacy\')\nnlp = nlhappy.load(\'path/nlp\')\npreds = []\nfor d in targs:\n    doc = nlp(d[\'text\'])\n    preds.append(doc)\neg = [Example(x,y) for x,y in zip(preds, targs)]\nbadcases, score = analysis_text_badcase(eg, return_prf=True)\nprint(badcases[0].x, badcases[0].x._.label)\nprint(badcases[0].y, badcases[0].y._.label)\n```\n> 部署\n- 直接用nlp开发接口部署\n- 转为onnx\n```python\nfrom nlhappy.models import BertTextClassification\nckpt = \'logs/path/ckpt\'\nmodel = BertTextClassification.load_from_ckeckpoint(ckpt)\nmodel.to_onnx(\'path/tc.onnx\')\nmodel.tokenizer.save_pretrained(\'path/tokenizer\')\n```\n</details>\n\n<details>\n<summary><b>实体抽取</b></summary>\n\nnlhappy支持嵌套和非嵌套实体抽取任务\n> 数据处理\n```python\nfrom nlhappy.utils.convert_doc import convert_spans_to_dataset\nfrom nlhappy.utils.make_doc import get_docs_from_docbin\nfrom nlhappy.utils.make_dataset import train_val_split\nimport nlhappy\n# 制作docs\nnlp = nlhappy.nlp()\ndocs = []\n# data为你自己格式的原始数据,按需修改\n# 只需设置doc.ents \n# 嵌套型实体设置doc.spans[\'all\']\nfor d in data:\n    doc = nlp(d[\'text\'])\n    # 非嵌套实体\n    ents = []\n    for ent in d[\'spans\']:\n        start = ent[\'start\']\n        end = ent[\'end\']\n        label = ent[\'label\']\n        span = doc.char_span(start, end, label)\n        ents.append(span)\n    doc.set_ents(ents)\n    docs.append(doc)\n    # 嵌套型实体\n    for ent in d[\'spans\']:\n        start = ent[\'start\']\n        end = ent[\'end\']\n        label = ent[\'label\']\n        span = doc.char_span(start, end, label)\n        doc.spans[\'all\'].append(span)\n    docs.append(doc)\n# 保存docs,方便后边badcase分析\ndb = DocBin(docs=docs, store_user_data=True)\n# 制作数据集\n# 如果文本过长可以设置句子级别数据集\nds = convert_spans_to_dataset(docs, sentence_level=False)\ndsd = train_val_split(ds, val_frac=0.2)\n# 可以转换为dataframe分析数据\ndf = dsd.to_pandas()\nmax_length = df[\'text\'].str.len().max()\n# 保存数据集,注意要保存到datasets/目录下\ndsd.save_to_disk(\'datasets/your_dataset_name\')\n```\n> 训练模型\n编写训练脚本\n- 单卡\n```bash\nnlhappy \\\ndatamodule=span_classification \\\ndatamodule.dataset=your_dataset_name \\\ndatamodule.max_length=2000 \\\ndatamodule.batch_size=2 \\\ndatamodule.plm=roberta-wwm-base \\\nmodel=global_pointer \\\nmodel.lr=3e-5 \\\nseed=22222\n```\n- 多卡\n```\nnlhappy \\\ntrainer=ddp \\\ndatamodule=span_classification \\\ndatamodule.dataset=dataset_name \\\ndatamodule.max_length=350 \\\ndatamodule.batch_size=2 \\\ndatamodule.plm=roberta-wwm-base \\\nmodel=global_pointer \\\nmodel.lr=3e-5 \\\nseed=22222\n```\n- 后台训练\n```\nnohup bash scripts/train.sh >/dev/null 2>&1 &\n```\n- 现在可以去[wandb官网](https://wandb.ai/)查看训练详情了, 并且会自动产生logs目录里面包含了训练的ckpt,日志等信息.\n> 构建自然语言处理流程,并添加组件\n```python\nimport nlhappy\n\nnlp = nlhappy.nlp()\n# 默认device cpu, 阈值0.8\nconfig = {\'device\':\'cuda:0\', \'threshold\':0.9, \'set_ents\':True}\ntc = nlp.add_pipe(\'span_classifier\', config=config)\n# logs文件夹里面训练的模型路径\nckpt = \'logs/experiments/runs/your_best_ckpt_path\'\ntc.init_model(ckpt)\ntext = \'文本\'\ndoc = nlp(text)\n# 查看结果\n# doc.ents 为非嵌套实体,如果有嵌套会选最大跨度实体\n# doc.spans[\'all\'] 可以包含嵌套实体\nprint(doc.text, doc.ents, doc.spans[\'all\'])\n# 保存整个流程\nnlp.to_disk(\'path/nlp\')\n# 加载\nnlp = nlhappy.load(\'path/nlp\')\n```\n> badcase分析\n```python\nimport nlhappy\nfrom nlhappy.utils.analysis_doc import analysis_ent_badcase, Example, analysis_span_badcase\nfrom nlhappy.utils.make_doc import get_docs_from_docbin\n\ntargs = get_docs_from_docbin(\'corpus/dataset_name/train.spacy\')\nnlp = nlhappy.load(\'path/nlp\')\npreds = []\nfor d in targs:\n    doc = nlp(d[\'text\'])\n    preds.append(doc)\neg = [Example(x,y) for x,y in zip(preds, targs)]\n# 非嵌套实体\nbadcases, score = analysis_ent_badcase(eg, return_prf=True)\nprint(badcases[0].x, badcases[0].x.ents)\nprint(badcases[0].y, badcases[0].y.ents)\n# 嵌套实体\nbadcases, score = analysis_span_badcase(eg, return_prf=True)\nprint(badcases[0].x, badcases[0].x.spans[\'all\'])\nprint(badcases[0].y, badcases[0].y.spans[\'all\'])\n```\n> 部署\n- 直接用nlp开发接口部署\n- 转为onnx\n```python\nfrom nlhappy.models import GlobalPointer\nckpt = \'logs/path/ckpt\'\nmodel = GlobalPointer.load_from_ckeckpoint(ckpt)\nmodel.to_onnx(\'path/tc.onnx\')\nmodel.tokenizer.save_pretrained(\'path/tokenizer\')\n```\n</details>\n\n<details>\n<summary><b>实体标准化</b></summary>\nTODO\n</details>\n\n<details>\n<summary><b>关系抽取</b></summary>\nTODO\n</details>\n\n<details>\n<summary><b>事件抽取</b></summary>\nTODO\n</details>\n\n<details>\n<summary><b>通用信息抽取</b></summary>\nTODO\n</details>\n\n<details>\n<summary><b>摘要</b></summary>\nTODO\n</details>\n\n<details>\n<summary><b>翻译</b></summary>\nTODO\n</details>',
    'author': 'wangmengdi',
    'author_email': '790990241@qq.om',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)

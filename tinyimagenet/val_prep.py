#!/usr/bin/env python
# coding: utf-8

# In[20]:


import pandas as pd
import os
import shutil


# In[6]:


data = pd.read_table('val_annotations.txt',header=None)


# In[11]:


data.head()


# In[15]:


class_ids = sorted(data[1].unique())


# In[16]:


len(class_ids)


# In[19]:


for class_id in class_ids:
    os.mkdir(os.path.join('images',class_id))


# In[26]:


files = data[0]
class_ids = data[1]


# In[27]:


for i,file in enumerate(files):
    shutil.move(os.path.join('images',file),os.path.join('images',class_ids[i]))


# In[ ]:





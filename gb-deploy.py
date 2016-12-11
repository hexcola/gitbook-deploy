#! python 2.7
import logging
import yaml
import os
import shutil
import subprocess
from datetime import datetime

# clean all files under dist exclude .git
def clean_deploy_dir(dir):
    try:
        logging.info('gb-deploy: start clean {0} folder ...'.format(dir))
        for item in os.listdir(dir):
            if item != '.git' and item !='.gitignore':
                src = dir + os.sep +item
                if os.path.isfile(src):
                    os.remove(src)
                elif os.path.isdir(src):       
                    shutil.rmtree(src)
        logging.info('gb-deploy: clean deploy folder finished.')

    except Exception, e:
        logging.error(str(e))

# copy all files under src to dist folder
def update_deploy_dir(dir):
    try:
        logging.info('gb-deploy: start update {0} folder ...'.format(dir))
        for item in os.listdir('_book'):
            if item != '.gitignore' and item != 'gb-deploy.py':
                src = '_book' + os.sep + item
                deploy_dir = dir + os.sep + item
                if os.path.isfile(src):
                    shutil.copyfile(src, deploy_dir)
                elif os.path.isdir(src):
                    shutil.copytree(src, deploy_dir)

        logging.info('gb-deploy: update deploy folder finished.')

    except Exception, e:
        logging.error(str(e))

# push update to git pages
def push_to_gh_pages(dir):
    original_dir = os.getcwd()
    try:
        # switch to the deploy folder  
        new_dir = original_dir + os.sep + dir    
        os.chdir(new_dir)
        logging.info('gb-deploy: switch to {0}'.format(new_dir))
        
        try:
            logging.info('gb-deploy: git add .')
            subprocess.call(['git', 'add', '.'])

            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logging.info('gb-deploy: git commit -m "update: {0}"'.format(current_time))
            subprocess.call(['git', 'commit', '-m', 'update: {0}'.format(current_time)])
            
            logging.info('gb-deploy: start push to git pages...')
            # subprocess.call(['git', 'push', 'origin', branch])
            subprocess.call(['git', 'push'])
            logging.info('gb-deploy: push to git pages finished.')
        except:
            logging.info('gb-deploy: ERROR push failed.'), sys.exc_info()[0]
        
        # switch to old folder
        os.chdir(original_dir)
        logging.info('gb-deploy: switch back to {0}, and current dir is {1}'.format(original_dir, os.getcwd()))

    except Exception, e:
        logging.error(str(e))
     

# replace image file links
def update_links(dir, original_txt, new_txt):
    for item in os.listdir(dir):
        if item.find('.html') !=-1:
            # read the file and replace "_asset/image" 
            # to "https://raw.githubusercontent.com/egrethub/essentials/gh-pages/_asset/image"
            temp = dir + os.sep + item
            filedata = None

            with open(temp, 'r') as file :
                filedata = file.read()

            print('gb-deploy: File {0} replace {1} to {2}'.format(temp, original_txt, new_txt ))
            # Replace the target string
            filedata = filedata.replace(original_txt, new_txt)

            # Write the file out again
            with open(temp, 'w') as file:
                file.write(filedata)


# ---------------------------------------------------------
# run it after gb build
# ---------------------------------------------------------

try:
    with open('gb-config.yml', 'r') as f:
        config = yaml.load(f)

        # do it 
        deploy_dir = config['deploy_dir']
        img_root = config['img_root']
        new_img_root ='https://raw.githubusercontent.com/{0}/{1}/{2}/{3}'.format(config['id'], config['project'], config['branch'], img_root)

        clean_deploy_dir(deploy_dir)

        update_deploy_dir(deploy_dir)

        print(img_root)
        print(new_img_root)

        update_links(deploy_dir,img_root, new_img_root)

        push_to_gh_pages(deploy_dir)


except Exception, e:
    logging.error(str(e))
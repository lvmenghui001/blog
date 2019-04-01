from src.views.include import *

def add_node(tree_dic,comment):
    if comment.parent_id is None:
        # 如果我是顶层，就放到这
        tree_dic[comment] = {}

    else:#循环当前整个dict，直到找到为止
        for k,v in tree_dic.items():
            if k.id == comment.parent_id:#找到了你爸
                #print("find dad.",comment)  #debug
                tree_dic[k][comment] = {}
            else:#进入下一层继续找
                #print("keeping going deeper...")   #debug
                add_node(v,comment)


def build_tree(comment_set):
    tree_dic = {}
    for comment in comment_set:
        add_node(tree_dic,comment)
    #print("tree_dic",tree_dic)   #debug
    return tree_dic

def render_tree_note(tree_dic,margin_val):
    #print("tree_note----", tree_dic, margin_val)  #debug
    html = ""
    for k, v in tree_dic.items():
        username = db.session.query(Users.username).filter(Users.id==k.comment_persion_id).first()[0]
        ele = "<div class='comment-note' style='margin-left:%spx'>" %margin_val  + "<span style='color:red'>%s</span>"%username + ":"\
              + "<span style='margin-left:20px'>%s</span>"%k.comment_content \
              + "<span style='margin-left:20px;color:gray'>回复时间：%s</span>" % k.comment_time \
              + "<a comment-id='%s' style='margin-left:20px; ' class='add-comment' aria-hidden='true'>回复</a>"%k.id\
              +"</div>"
        html += ele
        html += render_tree_note(v,margin_val+20)
    return html


def render_comment_tree(tree_dic):
    #print("tree_dic------->>",tree_dic)  #debug
    html = ""
    for k, v in tree_dic.items():
        username = db.session.query(Users.username).filter(Users.id == k.comment_persion_id).first()[0]
        ele = "<div class='root-comment'>" + "<span style='color:red;margin-left:0px'>%s</span>"%username + ":"\
              + "<span style='margin-left:20px'>%s</span>"%k.comment_content \
              + "<span style='margin-left:20px;color:gray'>评论时间：%s</span>"%k.comment_time \
              + "<a comment-id='%s' style='margin-left:20px' class='add-comment' aria-hidden='true'>回复</a>"%k.id\
              +"</div>"
        html += ele
        html += render_tree_note(v,20)
    return html



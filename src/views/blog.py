from flask import make_response
from src.views import comment_handler
from src.views.include import *
blog = Blueprint("blog", __name__)

def right_articles_info():
    # 所有的文章
    articles = db.session.query(Articles).filter().all()

    # 按点击量由高到低排取4条记录
    first_click_article = db.session.query(Articles).order_by(Articles.click_num.desc()).limit(1)
    sort_articles = db.session.query(Articles).order_by(Articles.click_num.desc()).limit(4)

    # 按时间由近到远,取最近的4条记录
    new_articles = db.session.query(Articles).order_by(Articles.publish_time.asc()).limit(2)

    # 特别推荐按点赞数由高到低取3条记录
    good_articles = db.session.query(Articles).order_by(Articles.praise_num.desc()).limit(3)
    return articles, first_click_article, sort_articles, new_articles, good_articles


@blog.route("/")
def index():
    try:
        username = session["username"]
    except:
        username = ""
    articles, first_click_article, sort_articles, new_articles, good_articles = right_articles_info()
    return render_template(
        "index.html",
        username            = username,
        articles            = articles,
        sort_articles       = sort_articles,
        first_click_article = first_click_article[0],
        new_articles        = new_articles,
        good_articles       = good_articles
    )

@blog.route("/list")
def list():
    try:
        username = session["username"]
    except:
        username = ""

    articles, first_click_article, sort_articles, new_articles, good_articles = right_articles_info()
    return render_template(
        "list.html",
        username=username,
        articles=articles,
        sort_articles=sort_articles,
        first_click_article=first_click_article[0],
        new_articles=new_articles,
        good_articles=good_articles
    )


def articleinfo():
    try:
        username = session["username"]
    except:
        username = ""
    article_id = request.args["article_id"]
    a = db.session.query(Articles).filter(Articles.id==article_id).first()
    a.click_num = a.click_num + 1
    db.session.commit()
    article = db.session.query(Articles).filter(Articles.id == article_id).first()  #当前文章
    article_ids =  db.session.query(Articles.id).all()  #所有文章的id
    this_article_index = article_ids.index((int(article_id),)) #当前文章的索引
    if this_article_index == 0:
        last_article = ""
    else:
        last_article_index = this_article_index-1
        last_article_id = article_ids[last_article_index][0]
        last_article = db.session.query(Articles).filter(Articles.id == last_article_id).first()
    if this_article_index == len(article_ids) - 1:
        next_article = ""
    else:
        next_article_index = this_article_index+1
        next_article_id = article_ids[next_article_index][0]
        next_article = db.session.query(Articles).filter(Articles.id == next_article_id).first()

    # 查询此作者是否为此篇文章点赞
    try:
        author = session["username"]
        author_id = db.session.query(Users.id).filter(Users.username == author).first()[0]
        praise_count = db.session.query(ArticlePraise).filter(ArticlePraise.article == article.id,
                                                              ArticlePraise.author == author_id).count()
    except:
        praise_count = 0


    # 查询本篇文章的总的评论数
    comment_count = db.session.query(Comments).filter(Comments.article_id==article_id, Comments.parent_id==None).count()
    # 查询本篇文章的总的点赞数
    total_count = db.session.query(ArticlePraise).filter(ArticlePraise.article == article.id).count()
    return username, article, last_article, next_article, praise_count, total_count, comment_count


@blog.route("/article")
def article():
    username, article, last_article, next_article, praise_count, total_count, comment_count = articleinfo()
    return render_template(
        "article.html",
        username     = username,
        article      = article,
        last_article = last_article,
        next_article = next_article,
        praise_count = praise_count,
        total_count  = total_count,
        comment_count = comment_count
    )

@blog.route("/get_comments")
def get_comments():
    article_id = request.args["article_id"]
    comments = db.session.query(Comments).filter(Comments.article_id==article_id).all()
    db.session.close()
    comment_tree = comment_handler.build_tree(comments)
    tree_html = comment_handler.render_comment_tree(comment_tree)
    return tree_html


@blog.route("/post_comment", methods=["POST"])
def post_comments():
    article_id = int(request.form["article_id"])
    comment_content = request.form["comment"]
    parent_id = int(request.form["parent_comment_id"])
    if parent_id == 0:
        parent_id = None
    import time
    ltime = time.localtime(time.time())
    comment_time = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
    comment_persion = session["username"]
    comment_persion = db.session.query(Users.id).filter(Users.username == comment_persion).first()[0]
    comment = Comments()
    comment.article_id = article_id
    comment.comment_content = comment_content
    comment.comment_persion_id = comment_persion
    comment.comment_time = comment_time
    comment.parent_id = parent_id
    try:
        db.session.add(comment)
        db.session.commit()
        if parent_id == None:
            res = "post-comment-success|" + "1"
        else:
            res = "post-comment-success|" + "0"
    except Exception as e:
        logging.info("post-comment-fail")
        res = "post-comment-fail"
    finally:
        db.session.close()
    return res


@blog.route("/praise_article")
def praise_article():
    count = request.args["count"]
    article_id = request.args["article_id"]
    try:
        author = session["username"]
    except:
        source_url = "http://127.0.0.1:8500/article?article_id=%s" % article_id
        return render_template("login.html", source_url=source_url)
    author_id = db.session.query(Users.id).filter(Users.username == author).first()[0]
    praise_count = db.session.query(ArticlePraise).filter(ArticlePraise.article == article_id, ArticlePraise.author == author_id).count()
    if count == '0':
        if praise_count == 0:  #如果此用户已为此文章点赞，刷新点赞数不会跟着增加
            ap = ArticlePraise()
            ap.article = article_id
            ap.author = author_id
            db.session.add(ap)
            db.session.commit()
            db.session.close()
            a = db.session.query(Articles).filter(Articles.id == article_id).first()
            a.praise_num = db.session.query(ArticlePraise).filter(ArticlePraise.article == article_id).count()
            db.session.commit()
            db.session.close()
    else:
        if praise_count != 0:
            ap = db.session.query(ArticlePraise).filter(ArticlePraise.article == article_id, ArticlePraise.author == author_id).first()
            db.session.delete(ap)
            db.session.commit()
            db.session.close()
    username, article, last_article, next_article, praise_count, total_count,comment_count = articleinfo()
    return render_template(
        "article.html",
        username=username,
        article=article,
        last_article=last_article,
        next_article=next_article,
        praise_count=praise_count,
        total_count=total_count,
        comment_count = comment_count
    )


@blog.route("/about")
def about():
    try:
        username = session["username"]
        return render_template("about.html", username=username)
    except:
        source_url = "http://127.0.0.1:8500/about"
        return render_template("login.html", source_url=source_url)


@blog.route("/gbook", methods=["POST", "GET"])
def gbook():
    if request.method == "GET":
        try:
            username = session["username"]
            gbooks = db.session.query(Gbooks).all()
            articles, first_click_article, sort_articles, new_articles, good_articles = right_articles_info()
            return render_template(
                "gbook.html",
                gbooks = gbooks,
                username = username,
                articles = articles,
                sort_articles = sort_articles,
                first_click_article = first_click_article[0],
                new_articles=new_articles,
                good_articles = good_articles
            )
        except:
            source_url = "http://127.0.0.1:8500/gbook"
            return render_template("login.html", source_url = source_url)
    else:
        gbook_content = request.form["content"]
        import time
        ltime = time.localtime(time.time())
        gbook_time = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
        gbook_persion = session["username"]
        gb = Gbooks()
        gb.gbook_content = gbook_content
        gb.gbook_persion = gbook_persion
        gb.gbook_time = gbook_time
        db.session.add(gb)
        db.session.commit()
        db.session.close()
        return redirect("/gbook")


@blog.route("/release", methods=["GET", "POST"])
def release():
    if request.method == "GET":
        try:
            username = session["username"]
            article_types = db.session.query(ArticleTypes).filter().all()
            # 按点击量由高到低排取4条记录
            first_click_article = db.session.query(Articles).order_by(Articles.click_num.desc()).limit(1)
            sort_articles = db.session.query(Articles).order_by(Articles.click_num.desc()).limit(4)
            db.session.close()
            return render_template(
                "release.html",
                username=username,
                article_types=article_types,
                first_click_article=first_click_article[0],
                sort_articles=sort_articles
            )
        except Exception as e:
            source_url = "http://127.0.0.1:8500/release"
            return render_template("login.html", source_url=source_url)
    else:
        title = request.form["title"]
        article_type = request.form["article_type"]
        public = request.form["blog_type"]
        description = request.form["description"]
        content = request.form["article_content"]
        picture = ""
        import time
        ltime = time.localtime(time.time())
        publish_time = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
        try:
            pic = request.files["picture"]
            random_num = random.randint(1, 10000)
            timeStr = time.strftime("%Y-%m-%d", ltime)
            filename = str(timeStr) + "_" +str(random_num) + "_" + pic.filename
            full_filename = "static/images/upload/" + filename
            pic.save(full_filename)
            picture = "../" + full_filename
        except:
            pass
        author = session["username"]
        author = db.session.query(Users.id).filter(Users.username==author).first()[0]
        click_num, praise_num = 0, 0
        article = Articles()
        article.title = title
        article.type = article_type
        article.description = description
        article.content = content
        article.picture = picture
        article.publish_time = publish_time
        article.author_id = author
        article.click_num = click_num
        article.praise_num = praise_num
        article.public = public
        db.session.add(article)
        db.session.commit()
        db.session.close()
        return redirect("/release")


@blog.route("/photo")
def photo():
    try:
        username = session["username"]
        return render_template("photo.html", username=username)
    except:
        source_url = "http://127.0.0.1:8500/photo"
        return render_template("login.html", source_url=source_url)


@blog.route("/time")
def time():
    try:
        username = session["username"]
        time_articles = db.session.query(Articles.publish_time, Articles.title, Articles.id).all()
        time_articles_list = []
        for one in time_articles:
            time_articles_list.append(
                {
                    "id": one.id,
                    "title": one.title,
                    "publish_time": str(one.publish_time)[:10]
                 }
            )
        return render_template("time.html", username=username, time_articles=time_articles_list)
    except Exception as e:
        source_url = "http://127.0.0.1:8500/time"
        return render_template("login.html", source_url=source_url)

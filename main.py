from flask import Flask, request, jsonify

from message import send_to_all

app = Flask(__name__)

edging = '----------------------------------------------------------------\n'


@app.route("/", methods=['GET', 'POST'])
def webhook():
    data = request.json

    # json contains an attribute that differenciates between the types, see
    # https://docs.gitlab.com/ce/user/project/integrations/webhooks.html
    # for more infos

    kind = data['object_kind']
    msg = 'false'
    if kind == 'push':
        msg = generatePushMsg(data)
    elif kind == 'tag_push':
        msg = generatePushMsg(data)
    elif kind == 'issue':
        msg = generateIssueMsg(data)
    elif kind == 'note':
        msg = generateCommentMsg(data)
    elif kind == 'merge_request':
        msg = generateMergeRequestMsg(data)
    elif kind == 'wiki_page':
        msg = generateWikiMsg(data)
    elif kind == 'pipeline':
        msg = generatePipelineMsg(data)
    elif kind == 'build':
        msg = generateBuildMsg(data)

    if msg != 'false':
        send_to_all(msg)

    return jsonify({'status': 'ok'})


def generatePushMsg(data):
    msg = '*{0} ({1}) - {2} new commits*\n' \
        .format(data['project']['name'], data['project']['default_branch'], data['total_commits_count'])
    for commit in data['commits']:
        msg += edging
        msg += commit['message'].rstrip()
        msg += '\n' + commit['url'].replace("_", "\_") + '\n'
    msg += edging
    return msg


def generateIssueMsg(data):
    action = data['object_attributes']['action']
    if action == 'open':
        assignees = ''
        for assignee in data.get('assignees', []):
            assignees += assignee['name'] + ' '
        msg = '*{0}* new issue for *{1}*:\n' \
            .format(data['project']['name'], assignees)
    elif action == 'reopen':
        assignees = ''
        for assignee in data.get('assignees', []):
            assignees += assignee['name'] + ' '
        msg = '*{0}* issue re-opened for *{1}*:\n' \
            .format(data['project']['name'], assignees)
    elif action == 'close':
        msg = '*{0}* issue closed by *{1}*:\n' \
            .format(data['project']['name'], data['user']['name'])
    elif action == 'update':
        assignees = ''
        for assignee in data.get('assignees', []):
            assignees += assignee['name'] + ' '
        msg = '*{0}* issue assigned to *{1}*:\n' \
            .format(data['project']['name'], assignees)

    msg += '[{0}]({1})'.format(data['object_attributes']['title'], data['object_attributes']['url'])
    return msg


def generateCommentMsg(data):
    ntype = data['object_attributes']['noteable_type']
    if ntype == 'Commit':
        return 'note to commit'
    elif ntype == 'MergeRequest':
        return 'note to MergeRequest'
    elif ntype == 'Issue':
        return 'note to Issue'
    elif ntype == 'Snippet':
        return 'note on code snippet'


def generateMergeRequestMsg(data):
    if data['object_attributes']['action'] == 'unapproved':
        return 'false'

    msg = '*project {0}\n{1} --> {2}\n{3} merge request*\n'.format(
        data['project']['name'],
        data['object_attributes']['source_branch'],
        data['object_attributes']['target_branch'],
        data['object_attributes']['action'].upper())

    msg += edging
    msg += '\n' + data['object_attributes']['url'].replace("_", "\_") + '\n'
    msg += '\n' + 'name: ' + data['user']['name']
    msg += '\n' + 'nickname: ' + data['user']['username'] + '\n'
    msg += edging
    return msg


def generateWikiMsg(data):
    return 'new wiki stuff'


def generatePipelineMsg(data):
    if data['object_attributes']['status'] == 'pending':
        return 'false'

    msg = '*project {0}*\n*branch {1}*\n'.format(
        data['project']['name'],
        data['object_attributes']['ref'],
        )

    msg += edging
    msg += f"\n*pipeline status: {data['object_attributes']['status']}*\n"
    msg += f"\n*name: {data['user']['name']}*\n"
    msg += f"*nickname: {data['user']['username']}*\n"
    msg += edging
    return msg


def generateBuildMsg(data):
    return 'new build stuff'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10111)

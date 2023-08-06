
# note: this is a hack so that we can access the client modules in the src/sahale directory
# from ..src.sahale.app import App
# sys.path.append('/Users/jessieyoung/workspace/sdk-python/src/sahale')


from app import App

def activity():
    return "hello world"

app = App("id", "user")
app.register_activity(activity, "activity")
#!/usr/bin/env python

import json
import datetime
from google.appengine.api import urlfetch

class UVa:
   userid = {
      1498,    #janson
      271633,  #stenly
      230537,  #patricia
      230534,  #rudy
      272593,  #erhem
      327438,  #kenneth
      324273,  #edwinner
      230526,  #geraldi
      329831,  #franky
      329838,  #freedy
      329848,  #adrian lewis
      326241,  #hendra liana
      322566,  #shella
      331044,  #dewi
      327396,  #jehoshaphat
      280440,  #felix
      327400,  #roberto
      230542,  #andre tirta
      348674,  #debora
      78850,   #hobert
      348679,  #danieal
      #850689,  #zakhayu
      850538,  #bella
      850535,  #yoferen
      850092,  #suryanto
      851423,  #felix gotama
      851420,  #cindy winata
      851443,  #ryan surjadi
      788998,  #fendy augusfian
      784174,  #kuncoro yoko
      851853,  #nicholas jovianto
      840938,  #calvin kwee
      779649,  #jimmy
      807088,  #amartha dimas
      859207,  #yogi
      851869,  #edwin SH
      859203,  #alfred
      899788,  #ricky effendi
      899790,  #steven (2016)
      899792,  #fonda
      899789,  #charles yuliansen
      899786,  #hengki pranoto
      900503,
      900536,
      900322,
   }

   baseurl = "https://uhunt.onlinejudge.org/api/"
   problem_baseurl = "http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem="
   username_baseurl = "https://uhunt.onlinejudge.org/id/"

   verdict = {
      10: "Submission error",
      15: "Can't be judge",
      20: "In queue",
      30: "Compile error",
      35: "Restricted function",
      40: "Runtime error",
      45: "Output limit",
      50: "Time limit",
      60: "Memory limit",
      70: "Wrong answer",
      80: "PresentationE",
      90: "Accepted",
   }

   def ranklist(self):
      # rank, name, username, accepted, nos, lastproblem, lastverdict, lastdatetime, uvarank
      retval = []
      ranklist_baseurl = self.baseurl + "ranklist/"
      lastsubmission_baseurl = self.baseurl + "subs-user-last/"

      for uid in self.userid:
         e = {"id": uid}

         # user basic info
         url = ranklist_baseurl + str(uid) + "/0/0"
         result = urlfetch.fetch(url)
         u = json.loads(result.content)

         e.update({"rank": u[0].get("rank")});
         e.update({"name": u[0].get("name")});
         e.update({"username": u[0].get("username")});
         e.update({"ac": u[0].get("ac")});
         e.update({"nos": u[0].get("nos")});
         e.update({"usernamelink": self.username_baseurl + str(uid)});

         # user last submission
         url = lastsubmission_baseurl + str(uid) + "/1"
         result = urlfetch.fetch(url)
         u = json.loads(result.content)
         if len(u.get("subs")) > 0:
            subs = u.get("subs")[0]
            e.update({"lastproblem": self.getProblemName(subs[1])});
            e.update({"lastverdict": self.getVerdict(subs[2])});
            e.update({"lastdatetime": self.getDatetime(subs[4])});
            e.update({"lastproblemlink": self.problem_baseurl + str(subs[1])});

         retval.append(e)

      retval = sorted(retval, key=lambda k: k["ac"], reverse=True)
      return retval

   def getProblemName(self, pid):
      url = self.baseurl + "p/id/" + str(pid)
      result = urlfetch.fetch(url)
      p = json.loads(result.content)
      return str(p.get("num")) + " - " + p.get("title")

   def getVerdict(self, vid):
      return self.verdict.get(vid)

   def getDatetime(self, dt):
      dt = int(dt) + 25200 # 7 hours local time
      return datetime.datetime.fromtimestamp(int(dt)).strftime('%d-%b-%Y %H:%M:%S')

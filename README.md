# sopel-karma
Sopel IRC bot plugin to modify and track user Karma. Intented for some interoperability with [Limnoria's karma](https://github.com/progval/Limnoria/tree/master/plugins/Karma).

### Setup

```bash
cd "~/.sopel/plugins/"
wget https://raw.githubusercontent.com/dowodenum/sopel-karma/main/karma.py
```

### Usage

From any channel the bot is in, or via privmsg (adjust from `.` to your bot's configured prefix)...

`load`, `wipekarma`, and `setkarma` commands must be run by a bot admin (you):
```
<you> /msg bot .load karma
<you> test++
<bot> test's karma is now 1
<you> .karma test
<bot> Karma for "test" has been increased 1 times and decreased 0 times for a total karma of 1.
<you> .wipekarma test
<bot> you: Karma for test has been wiped.
<you> .setkarma test 69 33
<bot> you: Karma set - nick: test inc: 69 dec: 33
<you> .karma test
<bot> Karma for "test" has been increased 69 times and decreased 33 times for a total karma of 36.
```

### Importing a database

In a private message to the Limnoria bot (and while identified with the bot as its owner):
```
!dump #channel import-me.dat
```

Then run (in bash, same directory as that .dat file - ~/supybot/data/ perhaps):
```
$ wget https://raw.githubusercontent.com/dowodenum/sopel-karma/main/parse.py
$ chmod +x ./parse.py
$ ./parse.py "import-me.dat" 5 > karma-list.txt
```
... where the quoted string is your database file and '5' is the increased-karma threshold you're filtering by (use 0 for everything). Note that this parse script will filter any entries which have spaces in them.

You will now have a list of commands to feed to the bot to effectively 'import' the Limnoria karma to Sopel's database. Time for spam!

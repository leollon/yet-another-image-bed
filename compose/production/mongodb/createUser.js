use imgbed4yourself;
db.createUser({
    user: "your_username",
    pwd: "your_password",
    roles: [{
        role: "readWrite",
        db: "imgbed4yourself"
    }]
})
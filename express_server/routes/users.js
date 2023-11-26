var express = require('express');
var router = express.Router();
var db = require('../lib/db.js');
var cors = require("cors");
var bodyParser = require('body-parser');

var corsOptions = {
  origin: ["http://localhost:3000"],
  methods: ["GET", "POST", "PUT", "DELETE"]
};

router.use(cors(corsOptions));
router.use(bodyParser.json())
router.use(bodyParser.urlencoded({extended:false}))
router.use(express.urlencoded({ extended: true }))

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

// 학생테이블 정보를 JSON 형태로 보내줍니다.
router.post('/sel_stu', function(req, res) {
  const stu_id = req.body.stu_id;

  // 학번을 입력했으면 해당 정보만 보내줍니다.
  if (stu_id) {
    db.query('select * from student where stu_id = ?', [stu_id], function(err, results) {
      if (err) throw err;
      console.log(results); // 서버 콘솔에 원본 형태를 보여줍니다.
      res.json(results); // JSON 형태로 결과를 보내줍니다.
    });
  } else {
    db.query('select * from student', function(err, results) {
      if (err) throw err;
      console.log(results);
      res.json(results);
    });
  }
});

// sel_att 기본형
// router.post('/sel_att', function(req, res) {
//   const class_code = req.body.class_code;
//   const query = 'select * from att where class_code = ?'

//   db.query(query, [class_code], function(err, results) {
//     if (err) throw err;
//     console.log(results);
//     res.json(results);
//   });
// });

// Class_code 를 입력해야만 정보를 불어올 수 있습니다.
// 테스트 데이터셋의 무선네트워크는 과목코드가 AA08 입니다.
router.post("/sel_att", (req, res) => {
  const class_code = req.body.class_code;
  const query = 'select student.stu_name, att.stu_id, att.att_state, att.att_way, att.att_date from att, student where att.stu_id = student.stu_id and att.class_code = ?;';

  db.query(query, [class_code], function(err, results) {
    if (err) throw err;
    console.log(results);
    res.json(results);
  });
});

module.exports = router;

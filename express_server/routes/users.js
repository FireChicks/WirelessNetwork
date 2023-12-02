var express = require('express');
var router = express.Router();
var db = require('../lib/db.js');
var cors = require("cors");
var bodyParser = require('body-parser');
var fs = require('fs'); // FS 모듈 추가
var path = require('path'); // Path 모듈 추가

var corsOptions = {
  origin: ["http://localhost:3000"],
  methods: ["GET", "POST", "PUT", "DELETE"]
};

router.use(cors(corsOptions));
router.use(bodyParser.json());
router.use(bodyParser.urlencoded({ extended: false }));
router.use(express.urlencoded({ extended: true }));

/* GET users listing. */
router.get('/', function (req, res, next) {
  res.send('respond with a resource');
});

router.get('/combined_info', function (req, res) {
  const query = `
      SELECT student.*, att.att_state, att.att_way, att.att_date, student.stu_pic
      FROM student
      LEFT JOIN att ON student.stu_id = att.stu_id
  `;

  db.query(query, function (err, results) {
    if (err) {
      console.error(err);
      res.status(500).json({ error: 'Server Error' });
      return;
    }

    // 결과 데이터를 가공하여 Base64로 인코딩된 이미지를 추가
    const updatedResults = results.map(student => {
      // student.stu_pic에는 이미지 이진 데이터가 들어있다고 가정
      const base64ImageData = Buffer.from(student.stu_pic).toString('base64');
      student.stu_pic = `data:image/png;base64,${base64ImageData}`;
      return student;
    });

    res.json(updatedResults);
  });
});



// 학생테이블 정보를 JSON 형태로 보내줍니다.
router.post('/sel_stu', function (req, res) {
  const stu_id = req.body.stu_id;

  // 학번을 입력했으면 해당 정보만 보내줍니다.
  if (stu_id) {
    db.query('select * from student where stu_id = ?', [stu_id], function (err, results) {
      if (err) throw err;
      console.log(results); // 서버 콘솔에 원본 형태를 보여줍니다.
      res.json(results); // JSON 형태로 결과를 보내줍니다.
    });
  } else {
    db.query('select * from student', function (err, results) {
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
router.get("/sel_att", (req, res) => {
  const class_code = req.body.class_code;
  //클래스코드를 1로 가정
  const query = 'SELECT student.stu_name, att.stu_id, att.att_state, att.att_way, att.att_date, att.img FROM att INNER JOIN student ON att.stu_id = student.stu_id WHERE att.class_code = 1';

  db.query(query, [class_code], function (err, results) {
    if (err) {
      console.error(err);
      res.status(500).json({ error: 'Server Error' });
      return;
    }
    console.log(results);
    // 결과 데이터를 가공하여 Base64로 인코딩된 이미지를 추가
    const updatedResults = results.map(result => {
      // att.img에는 이미지 이진 데이터가 들어있다고 가정
      const base64ImageData = Buffer.from(result.img).toString('base64');
      result.img = `data:image/png;base64,${base64ImageData}`;
      return result;
    });

    res.json(updatedResults);
  });
});

router.get("/sel_att/:att_date", (req, res) => {
  const att_date = req.params.att_date;

  const query = 'SELECT att.img FROM att WHERE att.att_date = ?';

  db.query(query, [att_date], function (err, results) {
    if (err) {
      console.error(err);
      res.status(500).json({ error: 'Server Error' });
      return;
    }
    console.log(results);
    // 결과 데이터를 가공하여 Base64로 인코딩된 이미지를 추가
    const updatedResults = results.map(result => {
      // att.img에는 이미지 이진 데이터가 들어있다고 가정
      const base64ImageData = Buffer.from(result.img).toString('base64');
      result.img = `data:image/png;base64,${base64ImageData}`;
      return result;
    });

    res.json(updatedResults);
  });
});



// 이미지 파일 목록을 반환하는 라우트
router.get('/face', function (req, res) {
  const directoryPath = path.join(__dirname, '../public/face'); // 이미지 디렉토리 경로 지정

  fs.readdir(directoryPath, function (err, files) {
    if (err) {
      res.status(500).send('서버에서 파일을 읽을 수 없습니다.');
      return;
    }

    // 파일 목록을 JSON 형태로 반환
    res.json(files);
  });
});

module.exports = router;
var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cors = require('cors'); // CORS 라이브러리 임포트

var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

var app = express();
var fs = require('fs');

app.use(cors());
app.use('/images', express.static('images'));
app.use('/face', express.static('face'));

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);

// 이미지 파일 목록을 반환하는 라우트
app.get('/images', function(req, res) {
  var directoryPath = path.join(__dirname, 'images');

  fs.readdir(directoryPath, function(err, files) {
    if (err) {
      res.status(500).send('서버에서 파일을 읽을 수 없습니다.');
      return;
    }

    // 파일 목록을 JSON 형태로 반환
    res.json(files);
  });
});

app.get('/face', function(req, res) {
  var directoryPath = path.join(__dirname, 'face');

  fs.readdir(directoryPath, function(err, files) {
    if (err) {
      res.status(500).send('서버에서 파일을 읽을 수 없습니다.');
      return;
    }

    // 파일 목록을 JSON 형태로 반환
    res.json(files);
  });
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;

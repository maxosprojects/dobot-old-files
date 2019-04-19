var express = require('express');
var dobotAjax = require('../public/javascripts/dobotAjax');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { dTip: 'Dobot demo' });
});

router.post('/ps_post', function(req, res, next) {
   dobotAjax.processCmd(req, res);
});

module.exports = router;

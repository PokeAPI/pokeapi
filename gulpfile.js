
var gulp 		= require('gulp'),
	plumber     = require('gulp-plumber'),
	jshint      = require('gulp-jshint'),
	stylish     = require('jshint-stylish'),
	concat      = require('gulp-concat'),
	flatten     = require('gulp-flatten'),
	browserSync = require('browser-sync').create(),
	uglify      = require('gulp-uglify');

var client = {

	html: {

		'partials': 'pokemon_v2/client/components/**/views/*.html'
	},

	scripts: [
		'pokemon_v2/client/app.js',
		'pokemon_v2/client/components/**/scripts/*-module.js',
		'pokemon_v2/client/components/**/scripts/*-routes.js',
		'pokemon_v2/client/components/**/scripts/*-filters.js',
		'pokemon_v2/client/components/**/scripts/*-service.js',
		'pokemon_v2/client/components/**/scripts/*-directive.js',
		'pokemon_v2/client/components/**/scripts/*-controller.js'	
	],
}

var out = {

	scripts: 'assets/js',

	partials: 'pokemon_v2/templates/partials'
}


gulp.task('html', function () {

    return gulp.src(client.html.partials)
    	.pipe(flatten())
		.pipe(gulp.dest(out.partials));
});


gulp.task('scripts', function () {

	return gulp.src(client.scripts)
		.pipe(plumber())
		.pipe(jshint())
		.pipe(jshint.reporter(stylish))
		.pipe(uglify())
		.pipe(concat('app.min.js'))
		.pipe(gulp.dest(out.scripts));
});


gulp.task('watch', function () {

	// gulp.watch(client.styles.src, ['styles']);
	gulp.watch(client.html.partials, ['html']);
	gulp.watch(client.scripts, ['scripts']);
});


gulp.task('sync', function () {

    browserSync.init({

		port       : 3000,
		// files      : server.all,
		logLevel   : 'info', // info, debug, warn ,silent
		// middleware : [fallback],
		proxy      : 'localhost:8000'
	})
});


gulp.task('default', ['html', 'scripts']);
gulp.task('start', ['default', 'watch', 'sync']);
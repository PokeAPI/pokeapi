
var gulp 		= require('gulp'),
	plumber     = require('gulp-plumber'),
	jshint      = require('gulp-jshint'),
	stylish     = require('jshint-stylish'),
	concat      = require('gulp-concat'),
	flatten     = require('gulp-flatten'),
	browserSync = require('browser-sync').create(),
	sass        = require('gulp-sass'),
	nano        = require('gulp-cssnano'),
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

	styles   : {
		
		src: [
			'pokemon_v2/client/components/core/styles/core.scss',
			'pokemon_v2/client/components/core/styles/!(core).scss',
			'pokemon_v2/client/components/!(core)/styles/*.scss'
		],

		includes: [
			'pokemon_v2/client/components/core/styles'
		]
	}
}

var out = {

	all: 'assets/pokemon_v2/**/*.*',
	scripts: 'assets/pokemon_v2/js',
	styles: 'assets/pokemon_v2/css',
	partials: 'assets/pokemon_v2/partials'
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


gulp.task('styles', function () {

	return gulp.src(client.styles.src)
		.pipe(plumber())
		.pipe(sass({
			outputStyle: 'expanded',
			includePaths: client.styles.includes
		}))
		.pipe(nano())
		.pipe(concat('app.min.css'))
		.pipe(gulp.dest(out.styles))
});


gulp.task('watch', function () {

	gulp.watch(client.styles.src, ['styles']);
	gulp.watch(client.html.partials, ['html']);
	gulp.watch(client.scripts, ['scripts']);
});


gulp.task('sync', function () {

    browserSync.init({

		port       : 3000,
		files      : out.all,
		logLevel   : 'info', // info, debug, warn ,silent
		// middleware : [fallback],
		proxy      : 'localhost:8000'
	})
});


gulp.task('default', ['html', 'scripts', 'styles']);
gulp.task('start', ['default', 'watch', 'sync']);
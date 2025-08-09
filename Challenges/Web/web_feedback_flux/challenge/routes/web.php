<?php

use App\Http\Controllers\FeedbackController;
use Illuminate\Support\Facades\Route;

Route::get('/', [FeedbackController::class, 'create'])->name('feedback.create');
Route::post('/', [FeedbackController::class, 'store'])->name('feedback.store');

Route::get('/feedback', [FeedbackController::class, 'index'])->name('feedback.index');
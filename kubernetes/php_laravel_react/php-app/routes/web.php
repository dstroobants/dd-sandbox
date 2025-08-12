<?php

use Illuminate\Support\Facades\Route;
use Inertia\Inertia;

// Health check endpoint for Kubernetes liveness probe
Route::get('/health', function () {
    return response()->json([
        'status' => 'ok',
        'timestamp' => now()->toISOString(),
        'service' => 'laravel-app'
    ], 200);
})->name('health');

Route::get('/testing/test1', function () {
    return response()->json([
        'status' => 'ok',
        'timestamp' => now()->toISOString(),
        'service' => 'laravel-app'
    ], 200);
})->name('test1');

Route::get('/testing/test2', function () {
    return response()->json([
        'status' => 'ok',
        'timestamp' => now()->toISOString(),
        'service' => 'laravel-app'
    ], 200);
})->name('test2');

Route::get('/', function () {
    return Inertia::render('welcome');
})->name('home');

Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});

require __DIR__.'/settings.php';
require __DIR__.'/auth.php';

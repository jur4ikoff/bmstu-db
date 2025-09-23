#!/bin/bash

# Создание 25 файлов по маске xx.sql

for i in {1..10}; do
    # Форматируем номер с ведущим нулем (01, 02, ..., 25)
    filename=$(printf "%02d.sql" $i)
    
    # Создаем файл с базовым содержимым
    cat > "$filename" << EOF
-- SQL файл $filename
-- Автоматически создан

SELECT 'Hello from $filename' as message;

EOF

    echo "Создан файл: $filename"
done

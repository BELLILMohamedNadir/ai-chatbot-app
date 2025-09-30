#!/bin/bash

echo "═══════════════════════════════════════════════════════════════"
echo "           AI CHATBOT PROJECT STRUCTURE ANALYSIS"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Function to count lines in a file
count_lines() {
    if [ -f "$1" ]; then
        wc -l < "$1" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

# Function to format file size
format_size() {
    local size=$1
    if [ $size -gt 1048576 ]; then
        echo "$(( size / 1048576 ))M"
    elif [ $size -gt 1024 ]; then
        echo "$(( size / 1024 ))K"
    else
        echo "${size}B"
    fi
}

# Backend Analysis
echo "📦 BACKEND (Python/FastAPI)"
echo "───────────────────────────────────────────────────────────────"

backend_total_lines=0

find apps/backend/app -name "*.py" -type f 2>/dev/null | while read file; do
    lines=$(count_lines "$file")
    size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")
    formatted_size=$(format_size $size)
    
    # Clean path for display
    display_path=$(echo $file | sed 's|apps/backend/||')
    printf "%-50s %6s lines  %8s\n" "$display_path" "$lines" "$formatted_size"
    backend_total_lines=$((backend_total_lines + lines))
done

echo ""
echo "Frontend (Next.js/TypeScript)"
echo "───────────────────────────────────────────────────────────────"

frontend_total_lines=0

# Frontend pages
echo ""
echo "📄 Pages:"
find frontend/src/app -name "*.tsx" -type f 2>/dev/null | while read file; do
    lines=$(count_lines "$file")
    size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")
    formatted_size=$(format_size $size)
    
    display_path=$(echo $file | sed 's|frontend/src/||')
    printf "%-50s %6s lines  %8s\n" "$display_path" "$lines" "$formatted_size"
done

# Frontend components
echo ""
echo "🧩 Components:"
find frontend/src/components -name "*.tsx" -type f 2>/dev/null | while read file; do
    lines=$(count_lines "$file")
    size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")
    formatted_size=$(format_size $size)
    
    display_path=$(echo $file | sed 's|frontend/src/||')
    printf "%-50s %6s lines  %8s\n" "$display_path" "$lines" "$formatted_size"
done

# Frontend hooks
echo ""
echo "🪝 Hooks:"
find frontend/src/hooks -name "*.ts" -o -name "*.tsx" -type f 2>/dev/null | while read file; do
    lines=$(count_lines "$file")
    size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")
    formatted_size=$(format_size $size)
    
    display_path=$(echo $file | sed 's|frontend/src/||')
    printf "%-50s %6s lines  %8s\n" "$display_path" "$lines" "$formatted_size"
done

# Frontend lib/api
echo ""
echo "📚 Libraries & API:"
find frontend/src/lib -name "*.ts" -type f 2>/dev/null | while read file; do
    lines=$(count_lines "$file")
    size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")
    formatted_size=$(format_size $size)
    
    display_path=$(echo $file | sed 's|frontend/src/||')
    printf "%-50s %6s lines  %8s\n" "$display_path" "$lines" "$formatted_size"
done

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "                        CODE QUALITY METRICS"
echo "═══════════════════════════════════════════════════════════════"

# Count total files
total_py=$(find apps/backend/app -name "*.py" -type f 2>/dev/null | wc -l)
total_tsx=$(find frontend/src -name "*.tsx" -type f 2>/dev/null | wc -l)
total_ts=$(find frontend/src -name "*.ts" -type f 2>/dev/null | wc -l)

echo ""
echo "📊 File Counts:"
echo "  Backend (Python):     $total_py files"
echo "  Frontend (TSX):       $total_tsx files"
echo "  Frontend (TS):        $total_ts files"
echo ""

# Check for files exceeding recommended lengths
echo "⚠️  Large Files (>300 lines):"
find apps/backend/app frontend/src -name "*.py" -o -name "*.ts" -o -name "*.tsx" -type f 2>/dev/null | while read file; do
    lines=$(count_lines "$file")
    if [ "$lines" -gt 300 ]; then
        display_path=$(echo $file | sed 's|apps/backend/||' | sed 's|frontend/src/||')
        printf "  %-50s %6s lines ⚠️\n" "$display_path" "$lines"
    fi
done

echo ""
echo "✅ Clean Code Principles:"
echo "  • Files under 300 lines: GOOD"
echo "  • Single Responsibility: Check large files"
echo "  • DRY (Don't Repeat Yourself): Review duplicates"
echo ""

echo "═══════════════════════════════════════════════════════════════"

#!/bin/bash
# Fetch 10 random pasta images and save to Pictures directory

DEST_DIR="/var/home/mirit/Afbeeldingen"

mkdir -p "$DEST_DIR"

for i in $(seq 1 10); do
    curl -sL "https://loremflickr.com/800/600/pasta" -o "$DEST_DIR/pasta_$i.jpg"
    if file "$DEST_DIR/pasta_$i.jpg" | grep -q "image"; then
        echo "Downloaded pasta_$i.jpg"
    else
        echo "Failed: pasta_$i.jpg (not an image)"
    fi
done

echo "Done! 10 pasta images saved to $DEST_DIR"
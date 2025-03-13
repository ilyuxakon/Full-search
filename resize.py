def resize(upperCorner, lowerCorner):
    x1, y1 = upperCorner.split()
    x2, y2 = lowerCorner.split()
    
    x1, y1, x2, y2, = float(x1), float(y1), float(x2), float(y2)
    
    width = (x1 - x2) * 1.5
    height = (y1 - y2) * 1.5
    
    return str(width), str(height)
# No external dependencies are required for this code.

class AABB:

    # private readonly epsilon = 0.0;
    # In Python, we use a class variable for a constant like this.
    # The 'readonly' concept is not enforced by the language, but the intent is preserved.
    _epsilon = 0.0


    def __init__(self, minX: float, minY: float, minZ: float, maxX: float, maxY: float, maxZ: float):
        self.minX = minX
        self.minY = minY
        self.minZ = minZ
        self.maxX = maxX
        self.maxY = maxY
        self.maxZ = maxZ


    def clone(self) -> 'AABB':
        return AABB(self.minX, self.minY, self.minZ, self.maxX, self.maxY, self.maxZ)


    def expand(self, x: float, y: float, z: float) -> 'AABB':
        minX = self.minX
        minY = self.minY
        minZ = self.minZ
        maxX = self.maxX
        maxY = self.maxY
        maxZ = self.maxZ


        # Handle expanding of min/max x
        if x < 0.0:
            minX += x
        else:
            maxX += x

        # Handle expanding of min/max y
        if y < 0.0:
            minY += y
        else:
            maxY += y

        # Handle expanding of min/max z
        if z < 0.0:
            minZ += z
        else:
            maxZ += z


        # Create new bounding box
        return AABB(minX, minY, minZ, maxX, maxY, maxZ)


    def grow(self, x: float, y: float, z: float) -> 'AABB':
        return AABB(self.minX - x, self.minY - y,
                self.minZ - z, self.maxX + x,
                self.maxY + y, self.maxZ + z)


    def clipXCollide(self, otherBoundingBox: 'AABB', x: float) -> float:
        # Check if the boxes are colliding on the Y axis
        if otherBoundingBox.maxY <= self.minY or otherBoundingBox.minY >= self.maxY:
            return x

        # Check if the boxes are colliding on the Z axis
        if otherBoundingBox.maxZ <= self.minZ or otherBoundingBox.minZ >= self.maxZ:
            return x

        # Check for collision if the X axis of the current box is bigger
        if x > 0.0 and otherBoundingBox.maxX <= self.minX:

            max_val = self.minX - otherBoundingBox.maxX - self._epsilon

            if max_val < x:
                x = max_val

        # Check for collision if the X axis of the current box is smaller
        if x < 0.0 and otherBoundingBox.minX >= self.maxX:

            max_val = self.maxX - otherBoundingBox.minX + self._epsilon

            if max_val > x:
                x = max_val

        return x

    def clipYCollide(self, otherBoundingBox: 'AABB', y: float) -> float:
        """
        Check for collision on the Y axis

        :param otherBoundingBox: The other bounding box that is colliding with the this one.
        :param y:                Position on the X axis that is colliding
        :return: Returns the corrected x position that collided.
        """
        # Check if the boxes are colliding on the X axis
        if otherBoundingBox.maxX <= self.minX or otherBoundingBox.minX >= self.maxX:
            return y

        # Check if the boxes are colliding on the Z axis
        if otherBoundingBox.maxZ <= self.minZ or otherBoundingBox.minZ >= self.maxZ:
            return y

        # Check for collision if the Y axis of the current box is bigger
        if y > 0.0 and otherBoundingBox.maxY <= self.minY:

            max_val = self.minY - otherBoundingBox.maxY - self._epsilon

            if max_val < y:
                y = max_val

        # Check for collision if the Y axis of the current box is bigger
        if y < 0.0 and otherBoundingBox.minY >= self.maxY:

            max_val = self.maxY - otherBoundingBox.minY + self._epsilon
            
            if max_val > y:
                y = max_val

        return y

    def clipZCollide(self, otherBoundingBox: 'AABB', z: float) -> float:
        """
        Check for collision on the Y axis

        :param otherBoundingBox: The other bounding box that is colliding with the this one.
        :param z:                Position on the X axis that is colliding
        :return: Returns the corrected x position that collided.
        """
        # Check if the boxes are colliding on the X axis
        if otherBoundingBox.maxX <= self.minX or otherBoundingBox.minX >= self.maxX:
            return z

        # Check if the boxes are colliding on the Y axis
        if otherBoundingBox.maxY <= self.minY or otherBoundingBox.minY >= self.maxY:
            return z

        # Check for collision if the Z axis of the current box is bigger
        if z > 0.0 and otherBoundingBox.maxZ <= self.minZ:
            max_val = self.minZ - otherBoundingBox.maxZ - self._epsilon
            # if (max < z) {
            #     z = max;
            # }
            if max_val < z:
                z = max_val

        # Check for collision if the Z axis of the current box is bigger
        if z < 0.0 and otherBoundingBox.minZ >= self.maxZ:
            max_val = self.maxZ - otherBoundingBox.minZ + self._epsilon
            if max_val > z:
                z = max_val

        return z

    def intersects(self, otherBoundingBox: 'AABB') -> bool:
        """
        Check if the two boxes are intersecting/overlapping

        :param otherBoundingBox: The other bounding box that could intersect
        :return: The two boxes are overlapping
        """
        # Check on X axis
        if otherBoundingBox.maxX <= self.minX or otherBoundingBox.minX >= self.maxX:
            return False

        # Check on Y axis
        if otherBoundingBox.maxY <= self.minY or otherBoundingBox.minY >= self.maxY:
            return False

        # Check on Z axis
        return (otherBoundingBox.maxZ > self.minZ) and (otherBoundingBox.minZ < self.maxZ)

    def move(self, x: float, y: float, z: float) -> None:
        """
        Move the bounding box relative.

        :param x: Relative offset x
        :param y: Relative offset y
        :param z: Relative offset z
        """
        # console.log(x, y, z)
        self.minX += x
        self.minY += y
        self.minZ += z
        self.maxX += x
        self.maxY += y
        self.maxZ += z

    def offset(self, x: float, y: float, z: float) -> 'AABB':
        """
        Create a new bounding box with the given offset

        :param x: Relative offset x
        :param y: Relative offset y
        :param z: Relative offset z
        :return: New bounding box with the given offset relative to this bounding box
        """
        return AABB(self.minX + x, self.minY + y, self.minZ + z, self.maxX + x, self.maxY + y, self.maxZ + z)

    def __repr__(self) -> str:
        return f"AABB [{self.minX} {self.maxX} : {self.minY} {self.maxY} : {self.minZ} {self.maxZ}] "
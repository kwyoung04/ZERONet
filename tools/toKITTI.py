import json
import sys
import numpy as np
import math

print("# SUS json to Kitti format")

class obj(object):
    def __init__(self, C):

        self.type       = C[0]
        self.truncation = float(C[1])
        self.occlusion  = int(C[2])
        self.alpha      = float(C[3])

        self.x1 = float(C[4])
        self.y1 = float(C[5])
        self.x2 = float(C[6])
        self.y2 = float(C[7])
        
        self.h      = float(C[8])
        self.w      = float(C[9])
        self.l      = float(C[10])
        self.t      = [float(C[11]), float(C[12]), float(C[13])]
        self.ry     = float(C[14])

        self.R = np.array([[math.cos(self.ry), 0, math.sin(self.ry)],
                           [0, 1, 0],
                           [-math.sin(self.ry), 0, math.cos(self.ry)]])
        self.x_corners = np.array([self.l/2, self.l/2, -self.l/2, -self.l/2, self.l/2, self.l/2, -self.l/2, -self.l/2])
        self.y_corners = np.array([0, 0, 0, 0, -self.h, -self.h, -self.h, -self.h])
        self.z_corners = np.array([self.w/2, -self.w/2, -self.w/2, self.w/2, self.w/2, -self.w/2, -self.w/2, self.w/2])

        self.corners_3D = np.dot(self.R, np.concatenate(([self.x_corners],
                                                         [self.y_corners],
                                                         [self.z_corners]), axis=0))
        self.corners_3D[0, :] += self.t[0]
        self.corners_3D[1, :] += self.t[1]
        self.corners_3D[2, :] += self.t[2]




def argc_json_dir():
    jsonPath = sys.argv[1]

    if len(sys.argv) != 3:
        print("Insufficient arguments")
        sys.exit()

    #return "/mnt/c/Users/Eric/Documents/openDataSet/testData/test2/label/001130.json"
    print("## source json file: ", jsonPath)
    return jsonPath



def json_decoding(sourceDir):
    with open(sourceDir, "r") as json_file:
        return json.load(json_file)



def write_txt(jsonName, strOut):
    txtPath = sys.argv[2]

    txtName = txtPath + '/' + jsonName + '.txt'

    #print("## target text file: ", txtName)
    print("### Box information to write to: ")
    print(strOut)

    with open(txtName, "w", encoding='utf-8') as f:
        f.write(strOut)


def trans_kitti_format():
    print("### label, truncated, occluded, alpha, bbox_xmin, bbox_ymin, bbox_xmax, bbox_xmin, dim_height, dim_width, dim_length, loc_x, loc_y, loc_z, rotation_y, score")
    pass
def heading_to_rot(heading):
    heading = float(heading)
    rot = -(np.pi / 2 + heading)
    return rot

def main():
    sourceDir = argc_json_dir()
    json_object = json_decoding(sourceDir)
    
    strFormat = '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n'
    strOut=""
    for individual in json_object:
        boxInfo = individual['psr']
        
        if (boxInfo['scale']['x'] < 0 or boxInfo['scale']['y'] < 0 or boxInfo['scale']['z'] < 0):
            continue

        strOut += strFormat %(individual['obj_type'],      # label
                              0.00,                        # truncated
                              0,                           # occluded
                              0,                       # alpha
                              0,                       # bbox_xmin
                              0,                      # bbox_ymin
                              0,                      # bbox_xmax
                              0,                      # bbox_ymax
                              boxInfo['scale']['z'] ,    # dim_height
                              boxInfo['scale']['y'] ,    # dim_width
                              boxInfo['scale']['x'] ,    # dim_length
                              boxInfo['position']['x'],       # loc_x
                              boxInfo['position']['y'],       # loc_y
                              boxInfo['position']['z'],     # loc_z
                              heading_to_rot(boxInfo['rotation']['z']))  # rotation_y
 

    #trans_kitti_format()

    jsonName = sourceDir.split('/')[-1][:-5]
    write_txt(jsonName, strOut)

    print("#### finished")



if __name__ == "__main__":
	main()


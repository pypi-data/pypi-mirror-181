from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter()

def WS(_type , _name , value , itr):
   writer.add_scalar(_type + '/' + _name, value, itr)
   
def WT(_type , _name , _str , itr):  
    writer.add_text(_type + '/' + _name, _str, itr)
    
def WG(pytorch_model , example_input):
   writer.add_graph(pytorch_model,example_input)
   
def WI(_type , _name , images , itr):
    import torchvision
    grid = torchvision.utils.make_grid(images)
    writer.add_image(_type + '/' + _name, grid, itr) 
    
def WC():
   writer.close()    
      